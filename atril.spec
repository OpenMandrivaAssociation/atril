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
Version:	1.8.0
Release:	1
License:	GPLv2+
Url:		http://mate-desktop.org/
Group:		Graphical desktop/Other
Source0:	http://pub.mate-desktop.org/releases/%{url_ver}/%{name}-%{version}.tar.xz
Patch0:		Check-for-NULL-in-synctex_backward_search.patch
Patch1:		atril-1.6.0-mga-Update-to-poppler-api-changes.patch
Patch2:		backends_-Fix-another-security-issue-in-the-dvi-backend.patch
Patch3:		backends_-Fix-several-security-issues-in-the-dvi-backend.patch
BuildRequires:	ghostscript
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	mate-common
BuildRequires:	yelp-tools
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(ddjvuapi)
BuildRequires:	pkgconfig(gail)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libcaja-extension)
BuildRequires:	pkgconfig(libsecret-1)
BuildRequires:	pkgconfig(libspectre)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(mate-icon-theme)
BuildRequires:	pkgconfig(poppler-glib)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(libgxps)
#gw just like xdvi, needed for rendering the fonts
BuildRequires:	kpathsea-devel
BuildRequires:	pkgconfig(ddjvuapi)

Requires:	ghostscript
Requires:	ghostscript-module-X
%rename %{oname}
Conflicts:	%{_lib}atril3 < 1.8.0-1

%description
Atril is the MATE Document viewer.

%package -n %{libname}
Group:		System/Libraries
Summary:	MATE Document viewer library

%description -n %{libname}
This is the MATE Document viewer library, the shared parts of %{name}.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}

%package -n %{devname}
Group:Development/C
Summary:	MATE Document viewer library
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This is the MATE Document viewer library, the shared parts of %{name}.

%prep
%setup -q
%apply_patches
NOCONFIGURE=1 ./autogen.sh

%build
%configure2_5x \
	--with-pic \
	--disable-static \
	--enable-introspection \
	--enable-pdf \
	--enable-tiff \
	--enable-djvu \
	--enable-dvi \
	--enable-pixbuf \
	--enable-comics \
	--enable-dvi \
	--enable-xps

%make

%install
%makeinstall_std

# remove of gsetting,convert file, no need for this in fedora
# because MATE starts with gsetting in fedora.
rm -fr %{buildroot}%{_datadir}/MateConf

%find_lang %{name} --with-gnome --all-name
cat %{name}.lang >> Atril.lang

%files -f Atril.lang
%doc README COPYING NEWS AUTHORS
%{_bindir}/*
%dir %{_datadir}/atril
%{_datadir}/atril/*
%{_datadir}/applications/atril.desktop
%{_iconsdir}/hicolor/*/apps/atril.*
%{_libexecdir}/atril-convert-metadata
%{_libexecdir}/atrild
%{_datadir}/dbus-1/services/org.mate.atril.Daemon.service
%{_datadir}/glib-2.0/schemas/org.mate.Atril.gschema.xml
%{_datadir}/thumbnailers/atril.thumbnailer
%{_mandir}/man1/atril-*.1*
%{_mandir}/man1/atril.1*

%{_libdir}/caja/extensions-2.0/libatril*so*
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

%files -n %{libname}
%{_libdir}/libatrildocument.so.%{major}*
%{_libdir}/libatrilview.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/AtrilDocument-%{api}.typelib
%{_libdir}/girepository-1.0/AtrilView-%{api}.typelib

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

