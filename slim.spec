Summary:	Shared Library Interface Macros
Summary(pl):	Makra dla interfejsów bibliotek dzielonych
Name:		slim
Version:	0.2.0
Release:	1
License:	BSD-like
Group:		Development/Libraries
Source0:	http://cairographics.org/snapshots/%{name}-%{version}.tar.gz
# Source0-md5:	acc800ad7b8dab6fe6c9a95dd38f4a4b
URL:		http://cairographics.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Shared Library Interface Macros used by Cairo library.

%description -l pl
SLIM (Shared Library Interface Macros) to makra dla interfejsów
bibliotek dzielonych, u¿ywane przez bibliotekê Cairo.

%prep
%setup -q

%build
%{__aclocal}
%{__automake}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README
%{_includedir}/*
%{_pkgconfigdir}/*.pc
