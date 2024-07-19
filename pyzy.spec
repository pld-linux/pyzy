#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	The Chinese PinYin and Bopomofo conversion library
Summary(pl.UTF-8):	Biblioteka konwersji pisma chińskiego PinYin i Bopomofo
Name:		pyzy
Version:	1.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/openSUSE/pyzy/releases
Source0:	https://github.com/openSUSE/pyzy/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	266a2d22e63b2df102b5f9f45d86d37f
Source1:	http://pyzy.googlecode.com/files/%{name}-database-1.0.0.tar.bz2
# Source1-md5:	d0951b8daa7f56a2cbd3b6b4e42532e0
Source2:	https://raw.githubusercontent.com/tsuna/boost.m4/3d67ee84e9149f6279a8df2113f5a86f0a83bd0d/build-aux/boost.m4
# Source2-md5:	86092bd75ae3e9109891646b21cc433e
URL:		https://github.com/openSUSE/pyzy
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	boost-devel >= 1.39
BuildRequires:	glib2-devel >= 1:2.24.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libuuid-devel
BuildRequires:	opencc-devel >= 1.0.2
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	sqlite3-devel
Requires:	glib2 >= 1:2.24.0
Suggests:	%{name}-db = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Chinese Pinyin and Bopomofo conversion library.

%description -l pl.UTF-8
Biblioteka konwersji pisma chińskiego PinYin i Bopomofo.

%package common
Summary:	Common files for pyzy and phrase databases
Summary(pl.UTF-8):	Pliki wspólne dla pyzy i baz danych fraz
Group:		Libraries
BuildArch:	noarch

%description common
Common files for pyzy and phrase databases.

%description common -l pl.UTF-8
Pliki wspólne dla pyzy i baz danych fraz.

%package devel
Summary:	Header files for pyzy library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki pyzy
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.24.0
Requires:	libstdc++-devel

%description devel
Header files for pyzy library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki pyzy.

%package static
Summary:	Static pyzy library
Summary(pl.UTF-8):	Statyczna biblioteka pyzy
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static pyzy library.

%description static -l pl.UTF-8
Statyczna biblioteka pyzy.

%package db-open-phrase
Summary:	The open phrase database for pyzy
Summary(pl.UTF-8):	Baza danych open-phrase dla pyzy
Group:		Libraries
Requires:	%{name}-common = %{version}-%{release}
Provides:	%{name}-db = %{version}-%{release}
Obsoletes:	ibus-pinyin-db-open-phrase < 1.4.99
BuildArch:	noarch

%description db-open-phrase
The phrase database for pyzy from open-phrase project.

%description db-open-phrase -l pl.UTF-8
Baza danych fraz dla pyzy pochodząca z projektu open-phrase.

%package db-android
Summary:	The android phrase database for pyzy
Summary(pl.UTF-8):	Baza danych android dla pyzy
Group:		Libraries
Requires:	%{name}-common = %{version}-%{release}
Provides:	%{name}-db = %{version}-%{release}
Obsoletes:	ibus-pinyin-db-android < 1.4.99
BuildArch:	noarch

%description db-android
The phrase database for pyzy from android project.

%description db-android -l pl.UTF-8
Baza danych fraz dla pyzy pochodząca z projektu android.

%prep
%setup -q

cp -pf %{SOURCE1} data/db/open-phrase

# update to support newer compilers
cp -pf %{SOURCE2} m4/boost.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-boost \
	--enable-db-open-phrase \
	--enable-opencc \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_libdir}/libpyzy-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpyzy-1.0.so.0

%files common
%defattr(644,root,root,755)
%dir %{_datadir}/pyzy
%{_datadir}/pyzy/phrases.txt
%dir %{_datadir}/pyzy/db
%{_datadir}/pyzy/db/create_index.sql

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpyzy-1.0.so
%{_includedir}/pyzy-1.0
%{_pkgconfigdir}/pyzy-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpyzy-1.0.a
%endif

%files db-open-phrase
%defattr(644,root,root,755)
%{_datadir}/pyzy/db/open-phrase.db

%files db-android
%defattr(644,root,root,755)
%{_datadir}/pyzy/db/android.db
