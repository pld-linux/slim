%define	cvs_release 20030830
Summary:	slim headers for Cairo
Name:		slim
Version:	0
Release:	0.%{cvs_release}.1
License:	BSD-like
Group:		Development/Libraries
Source0:	%{name}-cvs-%{cvs_release}.tar.gz
# Source0-md5:	229742924af4abfdc4cfc2e5c7ca15e8
URL:		http://cairographics.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
"slim" headers for Cairo

%prep
%setup -n %{name}

%build
%{__aclocal}
%{__automake} --add-missing
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_includedir}/*
%{_libdir}/pkgconfig/*
