Summary:	A Web frontend for the Direct Connect Text Client
Summary(pl):	Interfejs WWW do Direct Connect Text Client
Name:		phpdc
Version:	1.0
%define	_rc	rc1
Release:	0.%{_rc}.1
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}%{_rc}.tar.gz
# Source0-md5:	035a6a0dbedd55f724237aa0b9cebff9
Source1:        %{name}.conf
Patch0:		%{name}-config.patch
#		http://phpdc.sourceforge.net/release/phpdc-1.0rc1-hublist_bug.patch
Patch1:		%{name}-1.0rc1-hublist_bug.patch
URL:		http://phpdc.sourceforge.net/
Requires:	dctc
Requires:	php >= 4.3.0
Requires:	php-gd >= 4.3.0
Requires:	php-sockets >= 4.3.0
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_phpdcdir	%{_datadir}/%{name}
%define         _sysconfdir     /etc/%{name}


%description
PHPDC Web is a server-side Web frontend for the Direct Connect Text
Client (dctc).

%description -l pl
PHPDC Web to dzia³aj±cy po stronie serwera frontend WWW do tekstowego
klienta Direct Connect (dctc - Direct Connect Text Client).

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p0

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_phpdcdir}/{layout,private,styles,Downloads} \
        $RPM_BUILD_ROOT{%{_sysconfdir},/etc/httpd}


install *.php $RPM_BUILD_ROOT%{_phpdcdir}
install *.{html,png,ini} $RPM_BUILD_ROOT%{_phpdcdir}
install layout/* $RPM_BUILD_ROOT%{_phpdcdir}/layout
install private/* $RPM_BUILD_ROOT%{_phpdcdir}/private
install styles/* $RPM_BUILD_ROOT%{_phpdcdir}/styles

install phpdc.ini $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf %{_sysconfdir}/phpdc.ini $RPM_BUILD_ROOT%{_phpdcdir}/phpdc.ini


install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
        echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
        ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
        /usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
        umask 027
        if [ -d /etc/httpd/httpd.conf ]; then
                rm -f /etc/httpd/httpd.conf/99_%{name}.conf
        else
                grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
                        /etc/httpd/httpd.conf.tmp
                mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
                if [ -f /var/lock/subsys/httpd ]; then
                        /usr/sbin/apachectl restart 1>&2
                fi
        fi
fi

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
%dir %{_phpdcdir}
%dir %{_phpdcdir}/layout
%dir %{_phpdcdir}/private
%dir %{_phpdcdir}/styles
%attr(664,http,http) %dir %{_phpdcdir}/Downloads
%{_phpdcdir}/*.html
%{_phpdcdir}/*.php
%{_phpdcdir}/*.png
%{_phpdcdir}/layout/*
%{_phpdcdir}/private/*.php
%{_phpdcdir}/styles/*
%attr(664,root,http) %config(noreplace) %verify(not md5 size mtime) %{_phpdcdir}/private/phpdc.ini
