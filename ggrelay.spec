# $Revision: 1.11 $
Summary:	ggrelay - Gadu-Gadu instant messenger transparent proxy with DCC support
Summary(pl.UTF-8):   ggrelay - przezroczyste proxy dla komunikatora Gadu-Gadu z obsługą DCC
Name:		ggrelay
Version:	1.4
Release:	0.1
License:	GPL
Group:		Networking/Utilities
Source0:	http://dl.sourceforge.net/ggrelay/%{name}-%{version}.tar.gz
# Source0-md5:	46e1d32d2e809083a9fc8bfe9eb45b47
URL:		http://ggrelay.sourceforge.net/
Patch0:		%{name}-init.patch
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This small application is a simple GG relaying agent. This means, that
if you are a network administrator and applying masquerade on your
server, it's likely, that your customers would like to establish
direct connections over the masquerade using GG. This program is
intended to be the solution.

%description -l pl.UTF-8
Ta mała aplikacja jest prostym agentem przekazującym GG. Oznacza to,
że pozwala na używanie transferów plików pomiędzy użytkownikami
Gadu-Gadu, którzy schowani są za NAT-em (aka maskaradą).

%prep
%setup -q
%patch0 -p1

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
	echo "Installation completed."
	echo
	echo "1. Please adjust your /etc/sysconfig/ggrelay adding -o and possibly -i parameters."
	echo "2. Run \"/etc/rc.d/init.d/ggrelay start\" to start daemon."
	echo "3. Finally setup iptables to redirect connections:"
	echo "   \$ iptables -t nat -A PREROUTING -p tcp --dport 8074 -j REDIRECT"
	echo "   \$ iptables -I FORWARD -o <external iface> -d 217.17.41.0/24 -p+tcp --dport 443 -j REJECT"

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
%doc README*
%attr(755,root,root) %{_sbindir}/ggrelay
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ggrelay
%attr(754,root,root) /etc/rc.d/init.d/ggrelay
