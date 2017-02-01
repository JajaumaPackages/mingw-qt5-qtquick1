%?mingw_package_header

# Set this to one when mingw-qt5-qtwebkit isn't built yet
%global bootstrap 1

%global qt_module qtquick1
#%%global pre rc1

#%%global snapshot_date 20121111
#%%global snapshot_rev a14ab84c

%if 0%{?snapshot_date}
%global source_folder qt-%{qt_module}
%else
%global source_folder %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}
%endif

# first two digits of version
%global release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           mingw-qt5-%{qt_module}
Version:        5.5.1
Release:        4%{?pre:.%{pre}}%{?snapshot_date:.git%{snapshot_date}.%{snapshot_rev}}%{?dist}
Summary:        Qt5 for Windows - QtQuick1 component

License:        GPLv3 with exceptions or LGPLv2 with exceptions
Group:          Development/Libraries
URL:            http://www.qtsoftware.com/

%if 0%{?snapshot_date}
# To regenerate:
# wget http://qt.gitorious.org/qt/%{qt_module}/archive-tarball/%{snapshot_rev} -O qt5-%{qt_module}-%{snapshot_rev}.tar.gz
Source0:        qt5-%{qt_module}-%{snapshot_rev}.tar.gz
%else
%if "%{?pre}" != ""
Source0:        http://download.qt-project.org/development_releases/qt/%{release_version}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0:        http://download.qt-project.org/archive/qt/%{release_version}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif
%endif

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 96
BuildRequires:  mingw32-qt5-qtbase >= 5.5.1
BuildRequires:  mingw32-qt5-qtscript >= 5.5.1
BuildRequires:  mingw32-qt5-qttools >= 5.5.1
%if 0%{bootstrap} == 0
BuildRequires:  mingw32-qt5-qtwebkit >= 5.5.1
%endif

BuildRequires:  mingw64-filesystem >= 96
BuildRequires:  mingw64-qt5-qtbase >= 5.5.1
BuildRequires:  mingw64-qt5-qtscript >= 5.5.1
BuildRequires:  mingw64-qt5-qttools >= 5.5.1
%if 0%{bootstrap} == 0
BuildRequires:  mingw64-qt5-qtwebkit >= 5.5.1
%endif


%description
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win32
%package -n mingw32-qt5-%{qt_module}
Summary:        Qt5 for Windows - QtQuick1 component

%description -n mingw32-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win64
%package -n mingw64-qt5-%{qt_module}
Summary:        Qt5 for Windows - QtQuick1 component

%description -n mingw64-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


%?mingw_debug_package


%prep
%setup -q -n %{source_folder}


%build
%mingw_qmake_qt5 ../%{qt_module}.pro
%mingw_make %{?_smp_mflags}


%install
%mingw_make install INSTALL_ROOT=$RPM_BUILD_ROOT

# .prl files aren't interesting for us
find $RPM_BUILD_ROOT -name "*.prl" -delete

# The .dll's are installed in both %%{mingw32_bindir} and %%{mingw32_libdir}
# One copy of the .dll's is sufficient
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/*.dll
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/*.dll

# Prevent file conflict with mingw-qt4
mv $RPM_BUILD_ROOT%{mingw32_bindir}/qmlviewer.exe $RPM_BUILD_ROOT%{mingw32_bindir}/qmlviewer-qt5.exe
mv $RPM_BUILD_ROOT%{mingw64_bindir}/qmlviewer.exe $RPM_BUILD_ROOT%{mingw64_bindir}/qmlviewer-qt5.exe

# Create a list of .dll.debug files which need to be excluded from the main packages
# We do this to keep the %%files section as clean/readable as possible (otherwise every
# single file and directory would have to be mentioned individually in the %%files section)
# Note: the .dll.debug files aren't created yet at this point (as it happens after
# the %%install section). Therefore we have to assume that all .dll files will
# eventually get a .dll.debug counterpart
find $RPM_BUILD_ROOT%{mingw32_prefix} | grep .dll | grep -v .dll.a | sed s@"^$RPM_BUILD_ROOT"@"%%exclude "@ | sed s/".dll\$"/".dll.debug"/ > mingw32-qt5-%{qt_module}.excludes
find $RPM_BUILD_ROOT%{mingw64_prefix} | grep .dll | grep -v .dll.a | sed s@"^$RPM_BUILD_ROOT"@"%%exclude "@ | sed s/".dll\$"/".dll.debug"/ > mingw64-qt5-%{qt_module}.excludes


# Win32
%files -n mingw32-qt5-%{qt_module} -f mingw32-qt5-%{qt_module}.excludes
%{mingw32_bindir}/Qt5Declarative.dll
%{mingw32_bindir}/qml1plugindump.exe
%{mingw32_bindir}/qmlviewer-qt5.exe
%{mingw32_includedir}/qt5/QtDeclarative/
%{mingw32_libdir}/libQt5Declarative.dll.a
%{mingw32_libdir}/cmake/Qt5Declarative
%{mingw32_libdir}/cmake/Qt5Designer/Qt5Designer_QDeclarativeViewPlugin.cmake
%{mingw32_libdir}/pkgconfig/Qt5Declarative.pc
%{mingw32_libdir}/qt5/plugins/qml1tooling/
%{mingw32_libdir}/qt5/plugins/designer/qdeclarativeview.dll
%dir %{mingw32_datadir}/qt5/imports/
%{mingw32_datadir}/qt5/imports/Qt/
%if 0%{bootstrap} == 0
%{mingw32_datadir}/qt5/imports/QtWebKit/
%endif
%{mingw32_datadir}/qt5/imports/builtins.qmltypes
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_declarative.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_declarative_private.pri

# Win64
%files -n mingw64-qt5-%{qt_module} -f mingw64-qt5-%{qt_module}.excludes
%{mingw64_bindir}/Qt5Declarative.dll
%{mingw64_bindir}/qml1plugindump.exe
%{mingw64_bindir}/qmlviewer-qt5.exe
%{mingw64_includedir}/qt5/QtDeclarative/
%{mingw64_libdir}/libQt5Declarative.dll.a
%{mingw64_libdir}/cmake/Qt5Declarative
%{mingw64_libdir}/cmake/Qt5Designer/Qt5Designer_QDeclarativeViewPlugin.cmake
%{mingw64_libdir}/pkgconfig/Qt5Declarative.pc
%{mingw64_libdir}/qt5/plugins/qml1tooling/
%{mingw64_libdir}/qt5/plugins/designer/qdeclarativeview.dll
%dir %{mingw64_datadir}/qt5/imports/
%{mingw64_datadir}/qt5/imports/Qt/
%if 0%{bootstrap} == 0
%{mingw64_datadir}/qt5/imports/QtWebKit/
%endif
%{mingw64_datadir}/qt5/imports/builtins.qmltypes
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_declarative.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_declarative_private.pri


%changelog
* Wed Feb 01 2017 Jajauma's Packages <jajauma@yandex.ru> - 5.5.1-4
- Bootstrap build
- Update D/L URL to download.qt-project.org/archive

* Thu Apr  7 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.1-3
- Rebuild against mingw-qt5-qtbase 5.6.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 30 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.1-1
- Update to 5.5.1

* Fri Aug  7 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.0-1
- Update to 5.5.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 11 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.1-2
- Rebuild against latest mingw-gcc

* Mon Mar 23 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.1-1
- Update to 5.4.1

* Thu Jan  1 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.0-1
- Update to 5.4.0
- Added BR: mingw{32,64}-qt5-qtwebkit

* Sat Sep 20 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.2-1
- Update to 5.3.2

* Tue Jul  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.1-1
- Update to 5.3.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.0-1
- Update to 5.3.0

* Sun Mar 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.1-2
- Make sure we're built against mingw-qt5-qtbase >= 5.2.1 (RHBZ 1077213)

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.1-1
- Update to 5.2.1

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-4
- Previous commit caused .dll.a files to disappear

* Sun Jan 12 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-3
- Don't carry .dll.debug files in main package

* Wed Jan  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-2
- Dropped manual rename of import libraries

* Sun Jan  5 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-1
- Update to 5.2.0

* Fri Nov 29 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-0.1.rc1
- Update to 5.2.0 RC1

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.1-1
- Update to 5.1.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-1
- Update to 5.1.0

* Sun May 26 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.2-1
- Update to 5.0.2
- Added BR: mingw32-qt5-qttools mingw64-qt5-qttools
- Own the folders %%{mingw32_datadir}/qt5/imports and %%{mingw64_datadir}/qt5/imports

* Sat Feb  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.1-1
- Update to 5.0.1

* Fri Jan 11 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-1
- Update to Qt 5.0.0 Final

* Sun Nov 11 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.2.beta1.git20121111.a14ab84c
- Update to 20121111 snapshot (rev a14ab84c)
- Rebuild against latest mingw-qt5-qtbase
- Dropped pkg-config rename hack as it's unneeded now

* Mon Sep 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.1.beta1
- Initial release

