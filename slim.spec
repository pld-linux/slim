#
# TODO:
# - update slim-configuration.patch for pending WM-s
#
Summary:	SLiM - a desktop-independent graphical login manager
Summary(pl.UTF-8):	SLiM - niezależny od środowiska graficzny zarządca logowania
Name:		slim
Version:	1.3.5
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://download.berlios.de/slim/%{name}-%{version}.tar.gz
# Source0-md5:	1153e6993f9c9333e4cf745411d03472
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.pamd
Patch0:		%{name}-configuration.patch
Patch1:		cmake.patch
URL:		http://slim.berlios.de/
BuildRequires:	ConsoleKit-devel
BuildRequires:	cmake
BuildRequires:	dbus-devel
BuildRequires:	freeglut-devel
BuildRequires:	freetype-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 2:1.4.0
BuildRequires:	libstdc++-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	rpmbuild(macros) >= 1.450
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(post,postun):	systemd-units >= 38
Requires:	mktemp
Requires:	rc-scripts >= 0.4.0.10
Requires:	systemd-units >= 0.38
Requires:	xinitrc-ng >= 1.0
Provides:	XDM
Obsoletes:	slim-systemd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SLiM is a Desktop-independent graphical login manager for X11, derived
from Login.app.

It aims to be light and simple, although completely configurable
through themes and an option file; is suitable for machines on which
remote login functionalities are not needed.

Features included:
- PNG and XFT support for alpha transparency and antialiased fonts
- External themes support
- Configurable runtime options: X server, login / shutdown / reboot
  commands
- Single (GDM-like) or double (XDM-like) input control
- Can load predefined user at startup
- Configurable welcome / shutdown messages
- Random theme selection

%description -l pl.UTF-8
SLiM jest niezależnym od środowiska graficznym zarządcą ekranów dla
X11 wzorowanym na Login.app.

W założeniu ma być lekki i prosty, i jednocześnie całkowicie
konfigurowalny za pomocą motywów i pliku konfiguracyjnego; jest
przeznaczony dla maszyn, na których funkcjonalność zdalnego logowania
nie jest potrzebna.

Możliwości:
- obsługa PNG i XFT dla przezroczystości alpha oraz czcionek
  antyaliasowanych,
- wsparcie dla dodatkowych motywów,
- konfigurowalne opcje: serwer X, polecenia do logowania, wyłączania
  oraz restartu komputera,
- pojedyncza (jak w GDM) lub podwójna (jak w XDM) kontrola wejścia,
- możliwość automatycznego zalogowania danego użytkownika,
- konfigurowalne komunikaty powitania / pożegnania,
- losowy wybór motywu.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake \
	-DUSE_PAM=ON \
	-DUSE_CONSOLEKIT=ON \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir}/X11/slim \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{security,pam.d}
%{__make} -C build install \
	CFGDIR=%{_sysconfdir}/X11/slim \
	MANDIR=%{_mandir} \
	DESTDIR=$RPM_BUILD_ROOT

:> $RPM_BUILD_ROOT/etc/security/blacklist.slim
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/slim

# initscript
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,security}
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

# systemd
install -d $RPM_BUILD_ROOT%{systemdunitdir}
ln -s /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/slim.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add slim
# -n option not to actually restart as it will terminate all sessions opened from slim!
%service -n slim restart "SLiM Display Manager"
%banner -e %{name} <<EOF
NOTE: You need to prepare ~/.xinitrc to make slim work.
Take a look at %{_docdir}/%{name}-%{version}/xinitrc.sample*

EOF
%systemd_reload

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del slim
	%service slim stop
fi

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc ChangeLog README THEMES TODO xinitrc.sample
%dir %{_sysconfdir}/X11/slim
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/slim/slim.conf
%attr(754,root,root) /etc/rc.d/init.d/slim
%{systemdunitdir}/slim.service
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/slim
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.slim
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/slim
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/slim.1*
%{_datadir}/%{name}
