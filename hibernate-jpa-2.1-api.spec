%global namedreltag .Draft-16
%global namedversion %{version}%{?namedreltag}
%global oname hibernate-jpa-api
%global apiversion 2.1
Name:          hibernate-jpa-2.1-api
Version:       1.0.0
Release:       0.7.Draft.16%{?dist}
Summary:       Java Persistence 2.1 (JSR 338) API
License:       EPL and BSD
URL:           http://www.hibernate.org/
Source0:       https://github.com/hibernate/hibernate-jpa-api/archive/2.1-%{namedversion}.tar.gz
Source1:       http://repo1.maven.org/maven2/org/hibernate/javax/persistence/%{name}/%{namedversion}/%{name}-%{namedversion}.pom
# fix mvn build, this project uses the default Gradle to build
# sets various mvn plugins properties
Patch0:        %{oname}-2.1-1.0.0.Draft-16-pom.patch

BuildRequires: maven-local
BuildRequires: maven-plugin-bundle

BuildArch:     noarch

%description
Hibernate definition of the Java Persistence 2.1 (JSR 338) API.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{oname}-%{apiversion}-%{namedversion}
find . -name "*.jar" -delete

cp -p %{SOURCE1} pom.xml
%patch0 -p0

for s in src/main/java/javax/persistence/MapsId.java \
  src/main/java/javax/persistence/NamedStoredProcedureQuery.java \
  src/main/java/javax/persistence/EntityManager.java \
  src/main/java/javax/persistence/ForeignKey.java; do
 native2ascii -encoding UTF8 ${s} ${s}
done

# Fixing wrong-file-end-of-line-encoding
sed -i 's/\r//' src/main/javadoc/jdstyle.css

%mvn_file :%{name} %{name}

%build

%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license license.txt

%files javadoc -f .mfiles-javadoc
%license license.txt

%changelog
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