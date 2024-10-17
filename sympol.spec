# There is currently no check script because upstream's tests have bitrotted.
# Upstream has been informed of the situation.

Name:           sympol
Version:        0.1.8
Release:        9%{?dist}
Summary:        Symmetric polyhedra tool


License:        GPLv2+
URL:            https://www.math.uni-rostock.de/~rehn/software/sympol.html
Source0:        http://www.math.uni-rostock.de/~rehn/software/%{name}-%{version}.tar.gz
Source1:        http://www.math.uni-rostock.de/~rehn/software/%{name}-manual-0.1.pdf
Source10:       %{name}.rpmlintrc

BuildRequires:  bliss-devel
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  cddlib-devel
BuildRequires:  eigen3-static
BuildRequires:  gmpxx-devel
BuildRequires:  lrslib-devel
BuildRequires:  permlib-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
SymPol is a C++ tool to work with symmetric polyhedra.  It helps to
compute restricted automorphisms (parts of the linear symmetry group) of
polyhedra and performs polyhedral description conversion up to a given
or computed symmetry group.

%package libs
Summary:        Symmetric polyhedra library


%description libs
This package contains the SymPol library.

%package devel
Summary:        Headers and libraries for developing SymPol applications

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       boost-devel%{?_isa}
Requires:       eigen3-devel
Requires:       gmp-devel%{?_isa}
Requires:       permlib-devel

%description devel
This package contains the headers and library files needed to develop
SymPol applications.

%prep
%setup -q
cp -p %{SOURCE1} .

# Do not use the bundled cddlib, lrslib, or permlib
rm -fr external/{cddlib-094f,lrslib-042c,permlib}
sed -e "/(external/d" \
    -e "s|-O3 -g|-I%{_includedir}/cddlib -I%{_includedir}/lrslib -DBLISS_USE_GMP|" \
    -i CMakeLists.txt

# Eigen3 3.1.2 adds the need to link explicitly with -lpthread
sed -i 's/{Boost_LIBRARIES}/& pthread/' sympol/CMakeLists.txt
sed -i 's/{GMP_LIBRARIES}/& pthread/' test/CMakeLists.txt

%build
export LDFLAGS="$RPM_LD_FLAGS -Wl,--as-needed"
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo
make %{?_smp_mflags}

%install
make -C build install DESTDIR=$RPM_BUILD_ROOT

# Fix some header files with broken includes
cd $RPM_BUILD_ROOT%{_includedir}/%{name}
for f in *.h; do
  sed -r -e 's|(#include ").*/(.*")|\1\2|' -i.orig $f
  touch -r $f.orig $f
  rm -f $f.orig
done

%files
%doc %{name}-manual-0.1.pdf
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files libs
%doc AUTHORS COPYING
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}/

%changelog
* Mon Mar 10 2014 Jerry James <loganjerry@gmail.com> - 0.1.8-9
- Rebuild for eigen3-3.2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 0.1.8-7
- Rebuild for boost 1.54.0

* Sun Jul 21 2013 Rich Mattes <richmattes@gmail.com> - 0.1.8-6
- Rebuild for eigen3-3.1.3

* Wed Mar  6 2013 Jerry James <loganjerry@gmail.com> - 0.1.8-5
- Rebuild for eigen3-3.1.2

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.1.8-4
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.1.8-3
- Rebuild for Boost-1.53.0

* Wed Dec  5 2012 Jerry James <loganjerry@gmail.com> - 0.1.8-2
- Add -DBLISS_USE_GMP to CFLAGS to avoid segfaults

* Thu Sep 27 2012 Jerry James <loganjerry@gmail.com> - 0.1.8-1
- New upstream release

* Wed Sep 26 2012 Jerry James <loganjerry@gmail.com> - 0.1.7-3
- Rebuild for permlib 0.2.7

* Mon Aug 20 2012 Jerry James <loganjerry@gmail.com> - 0.1.7-2
- Move COPYING to the -libs subpackage

* Mon Apr 30 2012 Jerry James <loganjerry@gmail.com> - 0.1.7-1
- Initial RPM
