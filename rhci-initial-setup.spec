Summary: RHCI Initial system configuration utility
Name: rhci-initial-setup
URL: https://github.com/fusor/fusor-installer
Version: 0.0.2
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: GPLv2+
Group: System Environment/Base
BuildArch: noarch
BuildRequires: systemd-units
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: util-linux

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
%systemd_post initial-setup-text.service

%preun
%systemd_preun initial-setup-text.service

%postun
%systemd_postun_with_restart initial-setup-text.service

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
  
