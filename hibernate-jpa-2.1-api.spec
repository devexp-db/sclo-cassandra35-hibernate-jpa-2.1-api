%global namedreltag .Draft-16
%global namedversion %{version}%{?namedreltag}
%global oname hibernate-jpa-api
%global apiversion 2.1
Name:          hibernate-jpa-2.1-api
Version:       1.0.0
Release:       0.1.Draft.16%{?dist}
Summary:       Java Persistence 2.1 (JSR 338) API
Group:         Development/Libraries
License:       EPL and BSD
URL:           http://www.hibernate.org/
Source0:       https://github.com/hibernate/hibernate-jpa-api/archive/2.1-%{namedversion}.tar.gz
Source1:       http://repo1.maven.org/maven2/org/hibernate/javax/persistence/%{name}/%{namedversion}/%{name}-%{namedversion}.pom
# fix mvn build, this project uses the default Gradle to build
# sets various mvn plugins properties
Patch0:        %{oname}-2.1-1.0.0.Draft-16-pom.patch
BuildRequires: java-devel

BuildRequires: maven-local
BuildRequires: maven-compiler-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-plugin

Requires:      java
BuildArch:     noarch

%description
Hibernate definition of the Java Persistence 2.1 (JSR 338) API.

%package javadoc
Group:         Documentation
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

%build

mvn-rpmbuild package javadoc:aggregate

%install

mkdir -p %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{namedversion}.jar %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

# Fixing wrong-file-end-of-line-encoding
sed -i 's/\r//' target/site/apidocs/jdstyle.css
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp  target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc license.txt README.md

%files javadoc
%{_javadocdir}/%{name}
%doc license.txt

%changelog
* Thu May 09 2013 gil cattaneo <puntogil@libero.it> 1.0.0-0.1.Draft.16
- initial rpm