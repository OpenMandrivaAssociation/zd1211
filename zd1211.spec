%define build_dkms 1

%{?_with_dkms:%define build_dkms 1}
%{?_without_dkms:%define build_dkms 0}

%define	modname	zd1211
%define name	zd1211
%define	version	2.5.0.0
%define svnver	r67
%define	rel	0.%{svnver}.1
%define	release	%mkrel %{rel}

Name:           %{name}
Summary:        Userland tools for zd1211 driver
Version:        %{version}
Release:        %{release}
License:        GPL
Group:		System/Configuration/Hardware
URL:		http://zd1211.ath.cx/
Source0:        %{modname}-driver-%{svnver}.tar.bz2
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
%setup -q -n %{modname}-driver-%{svnver}
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

