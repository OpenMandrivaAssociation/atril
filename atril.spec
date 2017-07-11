%define url_ver %(echo %{version}|cut -d. -f1,2)
%define oname mate-document-viewer
%define build_dvi 1

%define api 1.5.0
%define major 3
%define girname	%mklibname %{name}-gir %{api}
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary:	MATE Document viewer
Name:		atril
Version:	1.18.0
Release:	1
License:	GPLv2+
Group:		Graphical desktop/Other
Url:		https://mate-desktop.org/
Source0:	https://pub.mate-desktop.org/releases/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	desktop-file-utils
BuildRequires:	ghostscript
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	mate-common
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(ddjvuapi)
BuildRequires:	pkgconfig(gail-3.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk+-unix-print-3.0)
BuildRequires:	pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(libcaja-extension)
BuildRequires:	pkgconfig(libgxps)
BuildRequires:	pkgconfig(libsecret-1)
BuildRequires:	pkgconfig(libspectre)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(mate-desktop-2.0)
BuildRequires:	pkgconfig(poppler-glib)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(webkit2gtk-4.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(zlib)
#gw just like xdvi, needed for rendering the fonts
BuildRequires:	kpathsea-devel
BuildRequires:	t1lib-devel
BuildRequires:	xsltproc
BuildRequires:	yelp-tools

Requires:	ghostscript
Requires:	ghostscript-module-X

%rename		%{oname}

%description
The MATE Desktop Environment is the continuation of GNOME 2. It provides an
intuitive and attractive desktop environment using traditional metaphors for
Linux and other Unix-like operating systems.

MATE is under active development to add support for new technologies while
preserving a traditional desktop experience.

This package provides Atril, the Document viewer for Mate desktop.

%files -f %{name}.lang
%doc README COPYING NEWS AUTHORS
%{_bindir}/*
%dir %{_datadir}/atril
%{_datadir}/atril/*
%{_datadir}/applications/atril.desktop
%{_iconsdir}/hicolor/*/apps/atril.*
%{_libexecdir}/atrild
%{_datadir}/dbus-1/services/org.mate.atril.Daemon.service
%{_datadir}/glib-2.0/schemas/org.mate.Atril.gschema.xml
%{_datadir}/thumbnailers/atril.thumbnailer
%{_datadir}/appdata/atril.appdata.xml
%{_mandir}/man1/atril-*.1*
%{_mandir}/man1/atril.1*
%{_libdir}/caja/extensions-2.0/libatril*so*
%{_datadir}/caja/extensions/libatril-properties-page.caja-extension
%dir %{_libdir}/%{name}/%{major}/
%dir %{_libdir}/%{name}/%{major}/backends
%{_libdir}/%{name}/%{major}/backends/lib*so*
%{_libdir}/%{name}/%{major}/backends/comicsdocument.%{name}-backend
%{_libdir}/%{name}/%{major}/backends/djvudocument.%{name}-backend
%{_libdir}/%{name}/%{major}/backends/xpsdocument.%{name}-backend
%{_libdir}/%{name}/%{major}/backends/dvidocument.%{name}-backend
%{_libdir}/%{name}/%{major}/backends/pdfdocument.%{name}-backend
%{_libdir}/%{name}/%{major}/backends/pixbufdocument.%{name}-backend
%{_libdir}/%{name}/%{major}/backends/psdocument.%{name}-backend
%{_libdir}/%{name}/%{major}/backends/tiffdocument.%{name}-backend
%{_libdir}/%{name}/%{major}/backends/epubdocument.atril-backend

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	MATE Document viewer library
Group:		System/Libraries

%description -n %{libname}
This package contains the shared libraries used by %{name}.

%files -n %{libname}
%{_libdir}/libatrildocument.so.%{major}*
%{_libdir}/libatrilview.so.%{major}*

#---------------------------------------------------------------------------

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
This package contains GObject Introspection interface library for %{name}.

%files -n %{girname}
%{_libdir}/girepository-1.0/AtrilDocument-%{api}.typelib
%{_libdir}/girepository-1.0/AtrilView-%{api}.typelib

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	MATE Document viewer library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains libraries and includes files for developing programs
based on %{name}.

%files -n %{devname}
%doc ChangeLog
%{_datadir}/gtk-doc/html/atril
%{_datadir}/gtk-doc/html/libatrildocument-%{api}
%{_datadir}/gtk-doc/html/libatrilview-%{api}
%{_libdir}/libatrildocument.so
%{_libdir}/libatrilview.so
%{_libdir}/pkgconfig/atril*pc
%{_includedir}/atril*
%{_datadir}/gir-1.0/AtrilDocument-%{api}.gir
%{_datadir}/gir-1.0/AtrilView-%{api}.gir

#---------------------------------------------------------------------------

%prep
%setup -q
%apply_patches

%build
%configure \
	--disable-schemas-compile \
	%{nil}
%make

%install
%makeinstall_std

# locales
%find_lang %{name} --with-gnome --all-name

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

