%define _disable_ld_no_undefined	1
%define _disable_ld_as_needed		1

%define buildgimpplugin	1

Summary: 	GPhoto2 GTK+ frontend
Name: 		gtkam
Version: 	0.1.16.1
Release: 	%{mkrel 1}
License: 	GPLv2+
Group: 		Graphics
Source0:	http://downloads.sourceforge.net/gphoto/%{name}-%{version}.tar.bz2
# file in the tarball is corrupt: replaced from upstream SVN. Drop
# with any release after 0.1.14. -AdamW 2007/07
Patch0:		gtkam-omf-install.patch
URL: 		http://sourceforge.net/projects/gphoto
Requires:	libgphoto-hotplug
BuildRequires: 	libgphoto-devel
BuildRequires: 	gettext-devel
BuildRequires: 	libexif-gtk-devel
BuildRequires:	autoconf
BuildRequires:	imagemagick
BuildRequires:	gnome-common
BuildRequires:	libbonobo2_x-devel
BuildRequires:	libbonobo-activation-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	scrollkeeper
%if %{buildgimpplugin}
BuildRequires: 	gimp-devel
%endif
BuildRoot: 	%{_tmppath}/%{name}-buildroot

Requires(post):		scrollkeeper
Requires(postun):	scrollkeeper

%description
GTKam is a fine interface for a wide variety of digital cameras.

%if %{buildgimpplugin}
%package gimp-plugin
Summary: 	GIMP-plug-in for digital camera access through GPhoto2
Requires: 	%{name} = %{version} 
Requires:	gimp
Group: 		Graphics

%description gimp-plugin
GIMP-plug-in for direct digital camera access through GPhoto2.
%endif

%prep
rm -rf %{buildroot}
%setup -q
%patch0 -p1

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
%if %mdkversion < 200900
%update_menus
%update_scrollkeeper
%endif
update-alternatives --install %{launchers}/kde.desktop camera.kde.dynamic %{launchers}/%{name}.desktop 50
update-alternatives --install %{launchers}/gnome.desktop camera.gnome.dynamic %{launchers}/%{name}.desktop 50

%postun
%if %mdkversion < 200900
%clean_menus
%clean_scrollkeeper
%endif
if [ $1 = 0 ]; then
  update-alternatives --remove camera.kde.dynamic %{launchers}/%{name}.desktop
  update-alternatives --remove camera.gnome.dynamic %{launchers}/%{name}.desktop
fi

%clean
rm -fr %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ABOUT-NLS AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%config(noreplace) %{launchers}/%{name}.desktop
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/images/%{name}
%{_datadir}/applications/*
%{_mandir}/*/%{name}*
%{_datadir}/omf/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}-camera.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%if %{buildgimpplugin}
%files gimp-plugin
%defattr(-,root,root,-)
%{_libdir}/gimp/*/plug-ins/%{name}-gimp
%endif
