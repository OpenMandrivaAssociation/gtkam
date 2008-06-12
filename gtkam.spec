%define name	gtkam
%define version	0.1.14

Summary: 	GPhoto2 GTK+ frontend
Name: 		%{name}
Version: 	%{version}
Release: 	%mkrel 3
License: 	GPL
Group: 		Graphics
Source0:	http://prdownloads.sourceforge.net/gphoto/%{name}-%{version}.tar.bz2
# file in the tarball is corrupt: replaced from upstream SVN. Drop
# with any release after 0.1.14. -AdamW 2007/07
Source1:	gtkam.png.bz2
Source2:	xmldocs.make.bz2
Patch4:		gtkam-omf-install.patch
URL: 		http://sourceforge.net/projects/gphoto
Requires:	libgphoto-hotplug
BuildRequires: 	libgphoto-devel
BuildRequires: 	gettext-devel
BuildRequires: 	libexif-gtk-devel
BuildRequires:	autoconf
BuildRequires:	ImageMagick
BuildRequires:	gnome-common libbonobo2_x-devel libbonobo-activation-devel libgnomeui2-devel
BuildRequires:	scrollkeeper
BuildRoot: 	%{_tmppath}/%{name}-buildroot
Requires(post): scrollkeeper
Requires(postun): scrollkeeper

%define buildgimpplugin 1

%if %{buildgimpplugin}
BuildRequires: 	gimp-devel
%endif

%description
GTKam is a fine interface for a wide variety of digital cameras.

%if %{buildgimpplugin}
%package gimp-plugin
Summary: 	GIMP-plug-in for digital camera access through GPhoto2
Requires: 	%name = %version 
Requires:	gimp
Group: 		Graphics

%description gimp-plugin
GIMP-plug-in for direct digital camera access through GPhoto2.
%endif

%prep
rm -rf %buildroot

%setup -q

%patch4 -p1
perl -pi -e 's,gimp/1.3/plug-ins,gimp/2.0/plug-ins,g' src/Makefile*
bzcat %{SOURCE1} > gtkam.png
bzcat %{SOURCE2} > xmldocs.make

%build

%configure2_5x

%make WARN_CFLAGS=""

%install
%makeinstall_std
%find_lang %{name} --with-gnome 

# icons
mkdir -p %buildroot%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
mkdir -p %buildroot%{_liconsdir}
mkdir -p %buildroot%{_miconsdir}
cp %buildroot%_datadir/pixmaps/%{name}.png %buildroot%{_iconsdir}/hicolor/48x48/apps/%{name}.png
cp %buildroot%_datadir/pixmaps/%{name}.png %buildroot%{_liconsdir}/%{name}.png
convert -scale 32 %buildroot%_datadir/pixmaps/%{name}.png %buildroot%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 32 %buildroot%_datadir/pixmaps/%{name}.png %buildroot%{_iconsdir}/%{name}.png
convert -scale 16 %buildroot%_datadir/pixmaps/%{name}.png %buildroot%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert -scale 16 %buildroot%_datadir/pixmaps/%{name}.png %buildroot%{_miconsdir}/%{name}.png
# menu stuff

mkdir -p %buildroot%{_datadir}/applications
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=GTKam
Comment=Access digital cameras (via GPhoto2)
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;Graphics;Photography;
EOF

rm -rf %buildroot%{_docdir}/%{name}
#rm -rf %buildroot/var/lib/scrollkeeper
rm -rf %buildroot/%{_datadir}/applications/gtkam.desktop

# dynamic desktop support
%define launchers /etc/dynamic/launchers/camera

mkdir -p %buildroot%launchers
cat > %buildroot%launchers/%name.desktop << EOF
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
update-alternatives --install %launchers/kde.desktop camera.kde.dynamic %launchers/%name.desktop 50
update-alternatives --install %launchers/gnome.desktop camera.gnome.dynamic %launchers/%name.desktop 50

%postun
%if %mdkversion < 200900
%clean_menus
%clean_scrollkeeper
%endif
if [ $1 = 0 ]; then
  update-alternatives --remove camera.kde.dynamic %launchers/%name.desktop
  update-alternatives --remove camera.gnome.dynamic %launchers/%name.desktop
fi

%clean
rm -fr %buildroot

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ABOUT-NLS AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%config(noreplace) %launchers/%{name}.desktop
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/images/%{name}
%{_datadir}/applications/*
%{_mandir}/*/%{name}*
%{_datadir}/omf/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%if %{buildgimpplugin}
%files gimp-plugin
%defattr(-,root,root,-)
%{_libdir}/gimp/*/plug-ins/%{name}-gimp
%endif
