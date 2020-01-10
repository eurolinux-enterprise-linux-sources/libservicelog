Name:           libservicelog
Version:        1.1.13
Release:        1%{?dist}
Summary:        Servicelog Database and Library

Group:          System Environment/Libraries
License:        LGPLv2
URL:            http://linux-diag.sourceforge.net/servicelog
Source0:        http://downloads.sourceforge.net/linux-diag/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(pre):       shadow-utils

BuildRequires:  sqlite-devel autoconf libtool bison librtas-devel flex

# because of librtas-devel
ExclusiveArch: ppc ppc64


# Link with needed libraries
Patch0: libservicelog-1.1.9-libs.patch

%description
The libservicelog package contains a library to create and maintain a
database for storing events related to system service.  This database
allows for the logging of serviceable and informational events, and for
the logging of service procedures that have been performed upon the system.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig sqlite-devel

%description    devel
Contains header files for building with libservicelog.


%prep
%setup -q
%patch0 -p1 -b .libs

%build
autoreconf -fiv
%configure --disable-static
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{__rm} -f %{buildroot}%{_libdir}/*.la


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group service >/dev/null || /usr/sbin/groupadd service

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING NEWS AUTHORS
%{_libdir}/libservicelog-*.so.*
%ghost %verify(not md5 size mtime) %attr(644,root,service) %dir /var/lib/servicelog/servicelog.db
%dir /var/lib/servicelog

%files devel
%defattr(-,root,root,-)
%{_includedir}/servicelog-1
%{_libdir}/*.so
%{_libdir}/pkgconfig/servicelog-1.pc


%changelog
* Sat May 18 2013 Vasant Hegde <hegdevasant@fedoraproject.org> - 1.1.13
- Update to latest upstream 1.1.13

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 08 2011 Jiri Skala <jskala@redhat.com> - 1.1.11-1
- update to latest upstream 1.1.11

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jun 04 2010 Roman Rakus <rrakus@redhat.com> - 1.1.9-4
- Properly handle servicelog.db

* Tue May 18 2010 Roman Rakus <rrakus@redhat.com> - 1.1.9-2
- Link with needed libraries (sqlite, rtas, rtasevent)

* Tue May 11 2010 Roman Rakus <rrakus@redhat.com> - 1.1.9-1
- Update to 1.1.9

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 31 2009 Roman Rakus <rrakus@redhat.com> - 1.0.1-2
- Added missing requires sqlite-devel in devel subpackage

* Fri Feb 20 2009 Roman Rakus <rrakus@redhat.com> - 1.0.1-1
- Initial packaging
