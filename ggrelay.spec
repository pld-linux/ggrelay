# $Revision: 1.2 $
Summary:	ggrelay - Gadu-Gadu instant messenger transparent proxy with DCC support
Summary(pl):	ggrelay - przezroczyste proxy dla komunikatora Gadu-Gadu z obs³ug± DCC
Name:		ggrelay
Version:	1.0rc5
Release:	1
License:	GPL
Group:		Networking/Utilities
Source0:	%{name}-%{version}.tar.gz
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
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
Gadu-Gadu, którzy schowani s± za NAT-em (aka maskarad±).

%prep
%setup -q

%build
%configure \
	--prefix="$RPM_BUILD_ROOT%{_prefix}"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install
./install.sh --rpmbuild "$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ggrelay
if [ -f /var/lock/subsys/ggrelay ]; then
	/etc/rc.d/init.d/ggrelay restart 1>&2
else
	echo
	echo "Installation completed. Please adjust your /etc/ggrelay/ggrelay.conf"
	echo "adding -o and possibly -i parameters."
	echo "Then run \"/etc/rc.d/init.d/ggrelay start\" to start daemon."
	echo
fi

%preun
if [ "$1" = 0 ]; then
	if [ -f /var/lock/subsys/ggrelay ]; then
		/etc/rc.d/init.d/ggrelay stop >&2
	fi
	/sbin/chkconfig --del ggrelay
fi

%files
%defattr(644,root,root,755)
%doc README COPYING
%attr(755,root,root) %{_sbindir}/ggrelay
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ggrelay
%attr(754,root,root) /etc/rc.d/init.d/ggrelay
