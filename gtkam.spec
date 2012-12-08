%define buildgimpplugin	1

Summary: 	GPhoto2 GTK+ frontend
Name: 		gtkam
Version: 	0.1.18
Release: 	1
License: 	GPLv2+
Group: 		Graphics
Source0:	http://downloads.sourceforge.net/gphoto/%{name}-%{version}.tar.bz2
# file in the tarball is corrupt: replaced from upstream SVN. Drop
# with any release after 0.1.14. -AdamW 2007/07
Patch0:		gtkam-omf-install.patch
Patch1:		gtkam_wformat.patch
URL: 		http://sourceforge.net/projects/gphoto
Requires:	libgphoto-hotplug
BuildRequires: 	libgphoto-devel
BuildRequires: 	gettext-devel
BuildRequires: 	libexif-gtk-devel
BuildRequires:	autoconf
BuildRequires:	imagemagick
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	pkgconfig(libbonobo-2.0)
BuildRequires:	pkgconfig(bonobo-activation-2.0)
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
%setup -q
%patch0 -p1
%patch1 -p1

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
#%{_datadir}/omf/%{name}
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


%changelog
* Fri Aug 31 2012 Vladimir Testov <vladimir.testov@rosalab.ru> 0.1.18-1
- new version 0.1.18

* Mon May 09 2011 Funda Wang <fwang@mandriva.org> 0.1.17-1mdv2011.0
+ Revision: 672675
- new version 0.1.17

* Sun May 08 2011 Funda Wang <fwang@mandriva.org> 0.1.16.1-3
+ Revision: 672484
- br intltool
- fix linkage

* Thu Sep 24 2009 Olivier Blin <oblin@mandriva.com> 0.1.16.1-2mdv2011.0
+ Revision: 448467
- fix wformat errors (from Arnaud Patard)
- remove unused xmldocs.make source
- rediff omf-install patch (from Arnaud Patard)

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Dec 09 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.16.1-1mdv2009.1
+ Revision: 312145
- drop old icons
- renumber the patch to 0
- drop sources which were to workaround corrupted files in a previous release
- new license policy
- new release 0.1.16.1
- small cleanups
- drop unnecessary defines

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.14-3mdv2008.1
+ Revision: 178962
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request
    - do not harcode icon extension
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Jul 05 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.14-1mdv2008.0
+ Revision: 48532
- rebuild for 2008
- use macros for scrollkeeper stuff
- drop old menu and X-Mandriva menu category
- add fd.o icons
- drop unnecessary manual requires on libgphoto2
- update gimp requires
- unversion autoconf buildrequires
- update icon from upstream SVN
- spec clean
- new release 0.1.14
- Import gtkam



* Fri Sep 01 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.1.13-3mdv2007.0
- Fix xdg menu

* Thu Aug 03 2006 Frederic Crozat <fcrozat@mandriva.com> 0.1.13-2mdv2007.0
- rebuild with latest dbus
- xdg menu

* Thu May 11 2006 Till Kamppeter <till@mandriva.com> 0.1.13-1mdk
- Updated to 0.1.13.
- Introduced %%mkrel.
- Removed patches 0-3.

* Thu Nov 03 2005 Frederic Crozat <fcrozat@mandriva.com> 0.1.12-10mdk
- Clean the scrollkeeper mess

* Wed Nov 02 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.1.12-9mdk
- Fix file section

* Fri Apr  1 2005 Till Kamppeter <till@mandrakesoft.com> 0.1.12-8mdk
- Added "Requires: libgphoto-hotplug" (bug 15135).

* Sat Nov 27 2004 Till Kamppeter <till@mandrakesoft.com> 0.1.12-7mdk
- Rebuilt for libexif-gtk5-0.3.5.

* Fri Sep 03 2004 Pascal Terjan <pterjan@mandrake.org> 0.1.12-6mdk
- oops, fix a typo in previous fix 

* Fri Sep 03 2004 Pascal Terjan <pterjan@mandrake.org> 0.1.12-5mdk
- fix xml path

* Mon Jul 19 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.12-4mdk
- fix descriptio

* Sat Jul 17 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.1.12-3mdk
- fix buildrequires and autotools usage

* Thu Jul 15 2004 Jerome Soyer <jeromesoyer@yahoo.fr> 0.1.12-2mdk
- Fixed xml code
- Added three patches (gimp 2, save, nodebug)
- Added "cp /usr/share/automake-1.8/depcomp ." before "automake --gnu", so
  that automake 1.8 works (Till Kamppeter).

* Sun Jul 11 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.1.12-1mdk
- 0.1.12

* Thu Sep 18 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.11-0.dev1.7mdk
- fix deps

* Thu Sep 11 2003 Till Kamppeter <till@mandrakesoft.com> 0.1.11-0.dev1.6mdk
- Changed icon to a digital photo camera icon (thanks to Fabian 
  Mandelbaum for the icon).

* Sat Aug 23 2003 Till Kamppeter <till@mandrakesoft.com> 0.1.11-0.dev1.5mdk
- Replaced icon by a preliminary camera icon (it is a video camera, a photo
  camera will come later).

* Sun Jul 27 2003 Till Kamppeter <till@mandrakesoft.com> 0.1.11-0.dev1.4mdk
- Rebuilt for libexif 0.5.10.

* Thu Jul 24 2003 Götz Waschk <waschk@linux-mandrake.com> 0.1.11-0.dev1.3mdk
- configure2_5x macro
- fix buildrequires and requires

* Fri Jul 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.1.11-0.dev1.2mdk
- buildrequires
- drop Prefix tag
- macroize
- quiet setup

* Thu Jun 12 2003 Till Kamppeter <till@mandrakesoft.com> 0.1.11-0.dev1.1mdk
- GTKam 0.1.11dev1.

* Fri Jan 17 2003 Till Kamppeter <till@mandrakesoft.com> 0.1.10-2mdk
- Rebuilt for new glibc and libexif.
- Removed dependency on libgpio.

* Thu Dec  5 2002 Till Kamppeter <till@mandrakesoft.com> 0.1.10-1mdk
- Updated to version 0.1.10.

* Tue Aug 13 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.1.9-2mdk
- added dynamic support

* Mon Aug  5 2002 Till Kamppeter <till@mandrakesoft.com> 0.1.9-1mdk
- Updated to version 0.1.9 (Move to GTK 2.x finished).

* Mon Jul 22 2002 Till Kamppeter <till@mandrakesoft.com> 0.1.8-2mdk
- Updated again to CVS from 22/07/2002 (progress bar for photo upload).

* Mon Jul 22 2002 Till Kamppeter <till@mandrakesoft.com> 0.1.8-1mdk
- Updated to CVS from 22/07/2002 (version 0.1.8+).
- Removed GIMP plug-in, it is only for GIMP 1.3.
- Added EXIF support.

* Wed Mar  6 2002 Till Kamppeter <till@mandrakesoft.com> 0.1-12mdk
- Updated to the CVS snapshot from 06/03/2002 (GTKam based on GPhoto2 2.0
  final).

* Sun Mar  3 2002 Till Kamppeter <till@mandrakesoft.com> 0.1-11mdk
- GTKam habla Español! Fabian Mandelbaum (fabman@mandrakesoft.com) has
  translated GTKam to spanish. Added the translation to the package.

* Mon Jan 28 2002 Till Kamppeter <till@mandrakesoft.com> 0.1-10mdk
- Rebuilt for libusb 0.1.4.

* Wed Jan 09 2002 David BAUDENS <baudens@mandrakesoft.com> 0.1-9mdk
- Add %%defattr(-,root,root,-) for gtkam-gimp-plugin

* Wed Jan 09 2002 David BAUDENS <baudens@mandrakesoft.com> 0.1-8mdk
- Fix menu entry

* Tue Dec  4 2001 Till Kamppeter <till@mandrakesoft.com> 0.1-7mdk
- Updated to the CVS snapshot from 04/12/2001.

* Sat Dec  1 2001 Till Kamppeter <till@mandrakesoft.com> 0.1-6mdk
- Updated to the CVS of 01/12/2001.

* Fri Nov 30 2001 Till Kamppeter <till@mandrakesoft.com> 0.1-5mdk
- Updated to the CVS of 30/11/2001.

* Mon Oct 08 2001 Stefan van der Eijk <stefan@eijk.nu> 0.1-4mdk
- BuildRequires: gettext-devel

* Thu Sep 13 2001 Stefan van der Eijk <stefan@eijk.nu> 0.1-3mdk
- fixed BuildRequires
- Copyright --> License

* Mon Aug  6 2001 Till Kamppeter <till@mandrakesoft.com> 0.1-2mdk
- Corrected the doc directory path again

* Mon Aug  6 2001 Till Kamppeter <till@mandrakesoft.com> 0.1-1mdk
- Moved to main
- Corrected the doc directory
- Added a menu entry
- Updated from CVS

* Mon Nov 27 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.1-0.20001116mdk
- new in contribs
- macros
- used srpm from rufus t firefly <rufus.t.firefly@linux-mandrake.com>
   - v0.1-0.20001116mdk (initial packaging from CVS) 
