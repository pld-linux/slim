%define	cvs_release 20030906
Summary:	slim headers for Cairo
Name:		slim
Version:	0.1.1
Release:	0.%{cvs_release}.1
License:	BSD-like
Group:		Development/Libraries
Source0:	%{name}-cvs-%{cvs_release}.tar.gz
Patch0:		%{name}-version.patch
# Source0-md5:	517699deb4a25a7789611feca3668f9c
URL:		http://cairographics.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
"slim" headers for Cairo

%prep
%patch0 -p0
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
