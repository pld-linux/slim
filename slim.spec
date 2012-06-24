Summary:	SLiM - a desktop-independent graphical login managaer
Summary(pl.UTF-8):   SLiM - niezależny od środowiska graficzny zarządca logowania
Name:		slim
Version:	1.2.6
Release:	2
License:	GPL v2
Group:		X11/Applications
Source0:	http://download.berlios.de/slim/%{name}-%{version}.tar.gz
# Source0-md5:	1bf891f046014a03236c21ce6cbe455b
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-Makefile.patch
URL:		http://slim.berlios.de/
BuildRequires:	freetype-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXrender-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	mktemp
Requires:	pam >= 0.99.7.1
Requires:	rc-scripts
Obsoletes:	gdm
Obsoletes:	kdm
Obsoletes:	wdm
Obsoletes:	xdm
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
X11 będącym

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

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	CFGDIR=%{_sysconfdir}/X11/slim

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	CFGDIR=%{_sysconfdir}/X11/slim \
	MANDIR=%{_mandir} \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/%{name}
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -D %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install -d $RPM_BUILD_ROOT/etc/security
:> $RPM_BUILD_ROOT/etc/security/blacklist.slim

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add slim
if [ -f /var/lock/subsys/slim ]; then
	echo "Run \"/sbin/service slim restart\" to restart slim." >&2
	echo "WARNING: it will terminate all sessions opened from slim!" >&2
else
	echo "Run \"/sbin/service slim start\" to start slim." >&2
fi

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del slim
	%service slim stop
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README THEMES TODO xinitrc.sample
%dir %{_sysconfdir}/X11/slim
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/slim/slim.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/slim
%attr(754,root,root) /etc/rc.d/init.d/slim
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.slim
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/slim
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/slim.1*
%{_datadir}/%{name}
