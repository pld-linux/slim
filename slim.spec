%define	cvs_release 20030906
Summary:	Shared Library Interface Macros
Summary(pl):	Makra dla interfejsów bibliotek dzielonych
Name:		slim
Version:	0.1.1
Release:	0.%{cvs_release}.1
License:	BSD-like
Group:		Development/Libraries
Source0:	%{name}-cvs-%{cvs_release}.tar.gz
Patch0:		%{name}-version.patch
# Source0-md5:	517699deb4a25a7789611feca3668f9c
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
%setup -n %{name}
%patch0 -p1

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
