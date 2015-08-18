Summary: Fusor Initial system configuration utility
Name: fusor-initial-setup
URL: https://github.com/fusor/fusor-initial-setup
Version: 0.0.20
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: GPLv2+
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: util-linux
Requires: fusor-installer
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
BuildArch: noarch

%description
The fusor-initial-setup utility runs after installation. It will automatically
invoke the fusor-installer upon reboot of a newly installed instance.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_datadir}/fusor-initial-setup/

cp bin/fusor-initial-setup %{buildroot}%{_bindir}/fusor-initial-setup
cp bin/fusor-initial-network-setup %{buildroot}%{_bindir}/fusor-initial-network-setup
cp bin/fusor-local-nfs-setup %{buildroot}%{_bindir}/fusor-local-nfs-setup
cp bin/foreman-discovery-image-repair.sh %{buildroot}%{_bindir}/foreman-discovery-image-repair.sh
cp bin/launch-fusor-installer %{buildroot}%{_bindir}/launch-fusor-installer
cp systemd/fusor-initial-setup-text.service %{buildroot}%{_unitdir}/fusor-initial-setup-text.service

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl enable fusor-initial-setup-text.service >/dev/null 2>&1 || :
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable fusor-initial-setup-text.service > /dev/null 2>&1 || :
    /bin/systemctl stop fusor-initial-setup-text.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart fusor-initial-setup-text.service >/dev/null 2>&1 || :
fi


%clean
rm -fr %{buildroot}

%files
%{_bindir}/fusor-initial-setup
%{_bindir}/fusor-initial-network-setup
%{_bindir}/fusor-local-nfs-setup
%{_bindir}/launch-fusor-installer
%{_bindir}/foreman-discovery-image-repair.sh
%{_unitdir}/fusor-initial-setup-text.service

%changelog
* Mon Apr 13 2015 John Matthews <jwmatthews@gmail.com> 0.0.20-1
- Updated to always attempt to remove the symlinks for foreman-discovery
  (jwmatthews@gmail.com)
- updated the file to include the .iso extension, and updated check for symlink
  name (jkim@localhost.localdomain)

* Mon Apr 13 2015 John Matthews <jwmatthews@gmail.com> 0.0.19-1
- Updated fusor-initial-setup to perform workaround for foreman-discovery-
  images (jwmatthews@gmail.com)

* Tue Jan 13 2015 John Matthews <jwmatthews@gmail.com> 0.0.18-1
- Updates from testing (jwmatthews@gmail.com)

* Tue Jan 13 2015 John Matthews <jwmatthews@gmail.com> 0.0.17-1
- Fix for name change of launch_fusor_installer (jwmatthews@gmail.com)

* Tue Jan 13 2015 John Matthews <jwmatthews@gmail.com> 0.0.16-1
- Adding ability to enable network and add an entry to /etc/hosts
  (jwmatthews@gmail.com)

* Sun Jan 11 2015 John Matthews <jwmatthews@gmail.com> 0.0.15-1
- Adding a hack to update /etc/hosts if hostname changed during install.
  (jwmatthews@gmail.com)

* Wed Dec 17 2014 John Matthews <jwmatthews@gmail.com> 0.0.14-1
- Update to call fusor-installer (jwmatthews@gmail.com)

* Thu Dec 11 2014 John Matthews <jwmatthews@gmail.com> 0.0.13-1
- Fix typo so we won't run katello-installer on every reboot
  (jwmatthews@gmail.com)

* Thu Dec 11 2014 John Matthews <jwmatthews@gmail.com> 0.0.12-1
- Commenting out ExecStartPost to see if it helps remove the recursive systemd
  call we've seen on firstboot (jwmatthews@gmail.com)

* Mon Dec 08 2014 John Matthews <jwmatthews@gmail.com> 0.0.11-1
- Updates from testing (jwmatthews@gmail.com)

* Mon Dec 08 2014 John Matthews <jwmatthews@gmail.com> 0.0.10-1
- Trying experiment of launching katello-installer from a gnome-terminal,
  instead of during boot process (jwmatthews@gmail.com)

* Mon Dec 08 2014 John Matthews <jwmatthews@gmail.com> 0.0.9-1
- Putting a temp change of waiting 5 mins before running katello-installer,
  thinking we may have a timing issue and need to adjust order of when fusor-
  initial-setup is kicked off (jwmatthews@gmail.com)

* Mon Dec 08 2014 John Matthews <jwmatthews@gmail.com> 0.0.8-1
- Working to get katello-installer to successfully run from systemd firstboot
  (jwmatthews@gmail.com)

* Fri Dec 05 2014 John Matthews <jwmatthews@gmail.com> 0.0.7-1
- Added a desktop shortcut for Firefox to connect to webui and Gedit to open
  katello-installer.log (jwmatthews@gmail.com)

* Fri Dec 05 2014 John Matthews <jwmatthews@gmail.com> 0.0.6-1
- Set HOME if not set, katello-installer requires this. When we run from
  systemd prior to user's logging in no HOME has been set, so we will default
  to /root if not set. (jwmatthews@gmail.com)

* Fri Dec 05 2014 John Matthews <jwmatthews@gmail.com> 0.0.5-1
- Testing disable of fusor-initial-setup after it's run once
  (jwmatthews@gmail.com)

* Fri Dec 05 2014 John Matthews <jwmatthews@gmail.com> 0.0.4-1
- Update path to katello-installer (jwmatthews@gmail.com)

* Fri Dec 05 2014 John Matthews <jwmatthews@gmail.com> 0.0.3-1
- fatal: bad revision 'fusor-initial-setup-0.0.2-1..HEAD'

* Tue Dec 02 2014 John Matthews <jwmatthews@gmail.com> 0.0.2-1
- new package built with tito

* Tue Dec 2 2014 John Matthews <jmatthews@redhat.com> - 0.0.1-1
- Initial packaging, based on Fedora's InitialSetup package
  
