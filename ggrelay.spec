# $Revision: 1.3 $
Summary:	ggrelay - Gadu-Gadu instant messenger transparent proxy with DCC support
Summary(pl):	ggrelay - przezroczyste proxy dla komunikatora Gadu-Gadu z obs�ug� DCC
Name:		ggrelay
%define 	_rc	rc5A
Version:	1.0
Release:	0.%{_rc}.1
License:	GPL
Group:		Networking/Utilities
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}-%{_rc}.tar.gz
#  Source0-md5:	7dd4ce85fdb72ad7c7f5d4156f386dc4
Patch0:		%{name}-init.patch
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
Ta ma�a aplikacja jest prostym agentem przekazuj�cym GG. Oznacza to,
�e pozwala na u�ywanie transer�w plik�w pomi�dzy u�ytkownikami
Gadu-Gadu, kt�rzy schowani s� za NAT-em (aka maskarad�).

%prep
%setup -q -n %{name}-%{version}-%{_rc}
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