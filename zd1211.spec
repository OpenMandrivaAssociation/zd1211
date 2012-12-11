%define build_dkms 1

%{?_with_dkms:%define build_dkms 1}
%{?_without_dkms:%define build_dkms 0}

%define	modname	%{name}
%define svnver	r85
%define	rel	0.%{svnver}.1

Name:		zd1211
Summary:	Userland tools for zd1211 driver
Version:	2.5.0.0
Release:	%mkrel %{rel}
License:	GPL
Group:		System/Configuration/Hardware
URL:		http://zd1211.ath.cx/
Source0:	%{modname}-driver-%{svnver}.tar.xz
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
%if %build_dkms
Requires:	dkms-%{name} = %{version}
%endif

%description
Initially contributed by ZyDAS under the GPL license, this ZD1211 Linux
driver is actively maintained by the open source community.

%if %build_dkms
%package -n	dkms-%{name}
Summary:	DKMS-ready kernel-source for the ZyDAS ZD1211 kernel module
License:	GPL
Group:		System/Kernel and hardware
Requires(pre):	dkms
Requires(post): dkms
Requires:	%{name} = %{version}

%description -n dkms-%{name}
Linux drivers for ZyDAS ZD1211 802.11b/g USB WLAN chipset.
DKMS package for %{name} kernel module.
%endif

%prep
%setup -q -n %{modname}
find -type f |xargs chmod 644

%build
gcc $RPM_OPT_FLAGS -o apdbg apdbg.c

%install
rm -rf $RPM_BUILD_ROOT
install -m755 -D apdbg %{buildroot}%{_sbindir}/apdbg

%if %build_dkms
mkdir -p $RPM_BUILD_ROOT/usr/src/%{modname}-%{version}-%{release}
cp -r * $RPM_BUILD_ROOT/usr/src/%{modname}-%{version}-%{release}
cat > %{buildroot}/usr/src/%{modname}-%{version}-%{release}/dkms.conf <<EOF

PACKAGE_VERSION="%{version}-%{release}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{modname}"
MAKE[0]="make -C \${kernel_source_dir} SUBDIRS=\${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build modules ZD1211REV_B=0"
CLEAN="make -C \${kernel_source_dir} SUBDIRS=\${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build clean"
BUILT_MODULE_NAME[0]="\$PACKAGE_NAME"
DEST_MODULE_LOCATION[0]="/kernel/drivers/usb/net/wireless"
REMAKE_INITRD="no"
EOF
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %build_dkms
%post -n dkms-%{name}
dkms add     -m %{modname} -v %{version}-%{release} --rpm_safe_upgrade
dkms build   -m %{modname} -v %{version}-%{release} --rpm_safe_upgrade
dkms install -m %{modname} -v %{version}-%{release} --rpm_safe_upgrade

%preun -n dkms-%{name}
dkms remove -m %{modname} -v %{version}-%{release} --rpm_safe_upgrade --all
%endif

%files
%defattr (-, root, root)
%doc sta
%{_sbindir}/apdbg

%if %build_dkms
%files -n dkms-%{name}
%defattr(-,root,root)
/usr/src/%{name}-%{version}-%{release}
%endif



%changelog
* Sat Oct 15 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.5.0.0-0.r85.1mdv2012.0
+ Revision: 704820
- fixed svn checkout
- new snapshot revision 85
  cleaned up specfile

* Mon Sep 21 2009 Thierry Vignaud <tv@mandriva.org> 2.5.0.0-0.r67.4mdv2010.0
+ Revision: 446316
- rebuild

* Fri Mar 06 2009 Antoine Ginies <aginies@mandriva.com> 2.5.0.0-0.r67.3mdv2009.1
+ Revision: 350035
- 2009.1 rebuild

* Thu Jan 03 2008 Olivier Blin <blino@mandriva.org> 2.5.0.0-0.r67.2mdv2008.1
+ Revision: 141006
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Oct 02 2007 Olivier Blin <blino@mandriva.org> 2.5.0.0-0.r67.2mdv2008.0
+ Revision: 94550
- rebuild for kmod provides
- import zd1211


* Thu Mar 30 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.5.0.0-0.r67.1mdk
- some cleanups and adaptions
- from Torbjorn Turpeinen tobbe@nyvalls.se> :
	o Initial release
