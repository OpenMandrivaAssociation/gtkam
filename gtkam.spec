%define buildgimpplugin	1

Summary:	GPhoto2 GTK+ frontend
Name:		gtkam
Version:	0.2.0
Release:	8
License:	GPLv2+
Group:		Graphics
Url:		http://sourceforge.net/projects/gphoto
Source0:	http://downloads.sourceforge.net/gphoto/%{name}-%{version}.tar.bz2
# file in the tarball is corrupt: replaced from upstream SVN. Drop
# with any release after 0.1.14. -AdamW 2007/07
Patch0:		gtkam-omf-install.patch
Patch1:		gtkam_wformat.patch

BuildRequires:	gnome-common
BuildRequires:	imagemagick
BuildRequires:	intltool
BuildRequires:	rarian
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(bonobo-activation-2.0)
BuildRequires:	pkgconfig(libbonobo-2.0)
BuildRequires:	pkgconfig(libexif-gtk)
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libgphoto2)
%if %{buildgimpplugin}
BuildRequires:	pkgconfig(gimp-2.0)
%endif
Requires(post,postun):	rarian
Requires:	libgphoto-common

%description
GTKam is a fine interface for a wide variety of digital cameras.

%if %{buildgimpplugin}
%package gimp-plugin
Summary:	GIMP-plug-in for digital camera access through GPhoto2
Group:		Graphics
Requires:	%{name} = %{version} 
Requires:	gimp

%description gimp-plugin
GIMP-plug-in for direct digital camera access through GPhoto2.
%endif

%prep
%setup -q
%apply_patches

%build
%configure2_5x

%make WARN_CFLAGS=""

%install
%makeinstall_std
%find_lang %{name} --with-gnome 

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
cp %{buildroot}%{_datadir}/pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 %{buildroot}%{_datadir}/pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{buildroot}%{_datadir}/pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# menu stuff
mkdir -p %{buildroot}%{_datadir}/applications
cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=GTKam
Comment=Access digital cameras (via GPhoto2)
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;Graphics;Photography;
EOF

rm -rf %{buildroot}%{_docdir}/%{name}
#rm -rf %{buildroot}/var/lib/scrollkeeper
rm -rf %{buildroot}/%{_datadir}/applications/gtkam.desktop

# dynamic desktop support
%define launchers /etc/dynamic/launchers/camera

mkdir -p %{buildroot}%{launchers}
cat > %{buildroot}%{launchers}/%{name}.desktop << EOF
[Desktop Entry]
Name=GTKam
Comment=GNU Digital Camera Program
TryExec=%{_bindir}/gtkam
Exec=%{_bindir}/gtkam
Terminal=false
Icon=gtkam
Type=Application
EOF

%post
update-alternatives --install %{launchers}/kde.desktop camera.kde.dynamic %{launchers}/%{name}.desktop 50
update-alternatives --install %{launchers}/gnome.desktop camera.gnome.dynamic %{launchers}/%{name}.desktop 50

%postun
if [ $1 = 0 ]; then
  update-alternatives --remove camera.kde.dynamic %{launchers}/%{name}.desktop
  update-alternatives --remove camera.gnome.dynamic %{launchers}/%{name}.desktop
fi


%files -f %{name}.lang
%doc ABOUT-NLS AUTHORS ChangeLog INSTALL NEWS README TODO
%config(noreplace) %{launchers}/%{name}.desktop
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/images/%{name}
%{_datadir}/applications/*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}-camera.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_mandir}/*/%{name}*

%if %{buildgimpplugin}
%files gimp-plugin
%{_libdir}/gimp/*/plug-ins/%{name}-gimp
%endif

