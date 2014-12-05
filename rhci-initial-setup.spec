Summary: RHCI Initial system configuration utility
Name: rhci-initial-setup
URL: https://github.com/fusor/fusor-installer
Version: 0.0.2
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: GPLv2+
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: util-linux
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
BuildArch: noarch

%description
The rhci-initial-setup utility runs after installation. It will automatically
invoke the rhci-installer upon reboot of a newly installed instance.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}

cp bin/rhci-initial-setup %{buildroot}%{_bindir}/rhci-initial-setup
cp systemd/rhci-initial-setup-text.service %{buildroot}%{_unitdir}/rhci-initial-setup-text.service

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl enable rhci-initial-setup-text.service >/dev/null 2>&1 || :
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable rhci-initial-setup-text.service > /dev/null 2>&1 || :
    /bin/systemctl stop rhci-initial-setup-text.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart rhci-initial-setup-text.service >/dev/null 2>&1 || :
fi


%clean
rm -fr %{buildroot}

%files
%{_bindir}/rhci-initial-setup
%{_unitdir}/rhci-initial-setup-text.service

%changelog
* Tue Dec 02 2014 John Matthews <jwmatthews@gmail.com> 0.0.2-1
- new package built with tito

* Tue Dec 2 2014 John Matthews <jmatthews@redhat.com> - 0.0.1-1
- Initial packaging, based on Fedora's InitialSetup package
  
