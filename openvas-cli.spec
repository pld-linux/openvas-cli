
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Open Vulnerability Assessment System CLI
Name:		openvas-cli
Version:	1.2.0
Release:	0.1
License:	GPL v2+
Group:		Applications
Source0:	http://wald.intevation.org/frs/download.php/1323/%{name}-%{version}.tar.gz
# Source0-md5:	e712eb71f3a13cc1b70b50f696465f8e
URL:		http://www.openvas.org/
BuildRequires:	cmake
BuildRequires:	glib2-devel >= 2.16
BuildRequires:	gnutls-devel > 2.8
BuildRequires:	openvas-libraries-devel >= 6.0.0
BuildRequires:	pkgconfig
%if %{with apidocs}
BuildRequires:	doxygen
#BuildRequires:	xmltoman
%endif
BuildConflicts:	openvas-libraries-devel >= 7.0
Requires:	openvas-common >= 6.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The module OpenVAS-CLI collects command line tools to handle with the
OpenVAS services via the respective protocols.

The best supported service is currently the OpenVAS-Manager
(openvasmd).

The Open Vulnerability Assessment System (OpenVAS) is a framework of
several services and tools offering a comprehensive and powerful
vulnerability scanning and vulnerability management solution.

%package apidocs
Summary:	OpenVAS CLI API documentation
Group:		Documentation

%description apidocs
OpenVAS CLI API documentation.

%package -n nagios-plugin-check_omp
Summary:	Nagios command plugin for the OpenVAS Management Protocol
Group:		Networking

%description -n nagios-plugin-check_omp
A nagios command plugin for the OpenVAS Management Protocol.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	-DLOCALSTATEDIR=/var \
	..
%{__make}

%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/nagios/plugins

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/nagios/plugins}/check_omp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES ChangeLog README
%doc doc/*.html
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man8/*.8*

%files -n nagios-plugin-check_omp
%defattr(644,root,root,755)
%{_libdir}/nagios/plugins/check_omp
