# $Revision: 1.1 $

Summary:	ggrelay is Gadu-Gadu instant messenger transparent proxy with DCC support.
Summary(pl):	ggrelay jest przezroczystym proxy dla komunkikatora Gadu-Gadu, ze swsparciem DCC.
Name:		ggrelay
Version:	1.0rc5
Release:	1
Group:		Networking/Utilities
License:	GPL
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This small application is a simple GG relaying agent. This means, that
if you are a network administrator and applying masquerade on your
server, it's likely, that your customers would like to establish
direct connections over the masquerade using GG. This program is
intended to be the solution.

%description -l pl
Ta ma³a aplikacja jest prostym agentem przekazuj±cym GG. Oznacza to,
¿e pozwala na u¿ywanie transerów plików pomiêdzy u¿ytkownikami
Gadu-Gadu, którzy schowani s± za NATem (aka maskarad±).

%prep
%setup -q

%build
%configure --prefix="$RPM_BUILD_ROOT%{_prefix}"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
rm -rf "$RPM_BUILD_ROOT"
mkdir "$RPM_BUILD_ROOT"
%{__make} install
./install.sh --rpmbuild "$RPM_BUILD_ROOT"

%post
/sbin/chkconfig --add ggrelay

echo
echo "Installation completed. Please adjust your /etc/ggrelay/ggrelay.conf"
echo "adding -o and possibly -i parameters."
echo

%postun
/sbin/service sshd condrestart > /dev/null 2>&1 || :

%preun
if [ "$1" = 0 ]; then
	/sbin/service ggrelay stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del ggrelay
fi

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(644,root,root,755)
%doc README COPYING
%config %{_sysconfdir}/ggrelay
/etc/rc.d/init.d/ggrelay
%attr(755,root,root) %{_sbindir}/ggrelay

$Log: ggrelay.spec,v $
Revision 1.1  2004-02-06 22:03:44  hunter
-initial pld spec.
