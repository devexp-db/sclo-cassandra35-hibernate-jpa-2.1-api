%{?scl:%scl_package hibernate-jpa-2.1-api}
%{!?scl:%global pkg_name %{name}}

%global namedreltag .Final
%global oname hibernate-jpa-api
%global apiversion 2.1
%global minversion 0
%global pkgversion %{?apiversion}%{?minversion}%{?namedreltag}
%global namedversion %{version}%{?namedreltag}

Name:		%{?scl_prefix}hibernate-jpa-2.1-api
Version:	1.0.0
Release:	3%{?dist}
Summary:	Java Persistence 2.1 (JSR 338) API
License:	EPL and BSD
URL:		http://www.hibernate.org/
Source0:	https://github.com/hibernate/%{oname}/archive/%{pkgversion}.tar.gz
Source1:	http://repo1.maven.org/maven2/org/hibernate/javax/persistence/%{pkg_name}/%{namedversion}/%{pkg_name}-%{namedversion}.pom
# fix mvn build, this project uses the default Gradle to build
# sets various mvn plugins properties
Patch0:		%{oname}-%{pkgversion}-pom.patch

BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_maven}maven-plugin-bundle
%{?scl:Requires: %scl_runtime}
BuildArch:	noarch

%description
Hibernate definition of the Java Persistence 2.1 (JSR 338) API.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{oname}-%{pkgversion}
find . -name "*.jar" -delete

cp -p %{SOURCE1} pom.xml
%patch0 -p1

# Fixing wrong-file-end-of-line-encoding
sed -i 's/\r//' src/main/javadoc/jdstyle.css

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_file :%{pkg_name} %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc README.md
%license license.txt

%files javadoc -f .mfiles-javadoc
%license license.txt

%changelog
* Wed Mar 01 2017 Tomas Repik <trepik@redhat.com> - 1.0.0-3
- scl conversion

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 06 2016 gil cattaneo <puntogil@libero.it> 1.0.0-1
- update to 1.0.0.Final

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-0.9.Draft.16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 gil cattaneo <puntogil@libero.it> - 1.0.0-0.8.Draft.16
- rebuilt

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.7.Draft.16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 05 2015 gil cattaneo <puntogil@libero.it> 1.0.0-0.6.Draft.16
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.5.Draft.16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.0.0-0.4.Draft.16
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.3.Draft.16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 08 2013 gil cattaneo <puntogil@libero.it> 1.0.0-0.2.Draft.16
- switch to XMvn
- minor changes to adapt to current guideline

* Thu May 09 2013 gil cattaneo <puntogil@libero.it> 1.0.0-0.1.Draft.16
- initial rpm
