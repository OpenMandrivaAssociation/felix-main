# Prevent brp-java-repack-jars from being run.
%define __jar_repack %{nil}

%global project felix
%global bundle org.apache.felix.main
%global groupId org.apache.felix
%global artifactId %{bundle}

Name:    %{project}-main
Version: 2.0.5
Release: 9
Summary: Apache Felix Main

Group:   Development/Java
License: ASL 2.0
URL:     http://felix.apache.org
Source0: http://www.apache.org/dist/felix/%{bundle}-%{version}-project.tar.gz

# TODO check availability and use original artifacts:
# - org.apache.felix.shell https://bugzilla.redhat.com/show_bug.cgi?id=615869
Patch0: %{bundle}-%{version}~pom.xml.patch
Patch1:	felix-main-pom.xml.fix_build.patch

BuildArch: noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: jpackage-utils
BuildRequires: felix-parent
BuildRequires: felix-osgi-compendium
BuildRequires: felix-osgi-core
BuildRequires: felix-framework
BuildRequires: maven2
BuildRequires:    maven-antrun-plugin
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-dependency-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-invoker-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-release-plugin
BuildRequires:    maven-resources-plugin
BuildRequires:    maven-surefire-plugin
BuildRequires:    maven-surefire-provider-junit4
# TODO check availability and use new names
#BuildRequires:    maven-bundle-plugin
# instead of
BuildRequires:    maven-plugin-bundle

Requires: felix-osgi-compendium
Requires: felix-osgi-core
Requires: felix-framework
Requires: java >= 0:1.6.0

Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

%description
Apache Felix Main Classes.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%global POM %{_mavenpomdir}/JPP.%{project}-%{bundle}.pom

%prep
%setup -q -n %{bundle}-%{version}
%patch0 -p1 -b .sav
%patch1 -p0 -b fix_build

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
%__mkdir_p $MAVEN_REPO_LOCAL
mvn-jpp -e \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}/%{project}
install -m 644 target/%{bundle}-%{version}.jar \
        %{buildroot}%{_javadir}/%{project}/%{bundle}.jar

%add_to_maven_depmap %{groupId} %{artifactId} %{version} JPP/%{project} %{bundle}

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{POM}

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
%__cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files
%defattr(-,root,root,-)
%{_javadir}/%{project}/*
%{POM}
%config(noreplace) %{_mavendepmapfragdir}/%{name}
%doc LICENSE

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}
%doc LICENSE

