Summary:	A Web frontend for the Direct Connect Text Client
Summary(pl):	Interfejs WWW do Direct Connect Text Client
Name:		phpdc
Version:	1.0
%define	_rc	rc1
Release:	0.%{_rc}.1
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}%{_rc}.tar.gz
Patch0:		%{name}-config.patch
URL:		http://phpdc.sourceforge.net/
Requires:	dctc
Requires:	php >= 4.3.0
Requires:	php-gd >= 4.3.0
Requires:	php-sockets >= 4.3.0
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_phpdir	/home/services/httpd/html/phpdc

%description
PHPDC Web is a server-side Web frontend for the Direct Connect Text
Client (dctc).

%prep
%setup -q -n %{name}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_phpdir}/{layout,private,styles}

install *.php $RPM_BUILD_ROOT%{_phpdir}
install *.{html,png,ini} $RPM_BUILD_ROOT%{_phpdir}
install layout/* $RPM_BUILD_ROOT%{_phpdir}/layout
install private/* $RPM_BUILD_ROOT%{_phpdir}/private
install styles/* $RPM_BUILD_ROOT%{_phpdir}/styles

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_phpdir}
%dir %{_phpdir}/layout
%dir %{_phpdir}/private
%dir %{_phpdir}/styles
%{_phpdir}/*.html
%{_phpdir}/*.php
%{_phpdir}/*.png
%{_phpdir}/layout/*
%{_phpdir}/private/*.php
%{_phpdir}/styles/*
%attr(664,root,http) %config(noreplace) %verify(not md5 size mtime) %{_phpdir}/private/phpdc.ini
