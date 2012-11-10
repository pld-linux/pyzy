#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	The Chinese PinYin and Bopomofo conversion library
Summary(pl.UTF-8):	Biblioteka konwersji pisma chińskiego PinYin i Bopomofo
Name:		pyzy
Version:	0.1.0
Release:	3
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: http://code.google.com/p/pyzy/downloads/list
Source0:	http://pyzy.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	73afc3c20808af2fee5f9fca47c64630
Source1:	http://pyzy.googlecode.com/files/%{name}-database-1.0.0.tar.bz2
# Source1-md5:	d0951b8daa7f56a2cbd3b6b4e42532e0
URL:		http://code.google.com/p/pyzy
BuildRequires:	boost-devel >= 1.39
BuildRequires:	glib2-devel >= 1:2.24.0
BuildRequires:	libstdc++-devel
BuildRequires:	libuuid-devel
BuildRequires:	opencc-devel
BuildRequires:	pkgconfig
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description db-android
The phrase database for pyzy from android project.

%description db-android -l pl.UTF-8
Baza danych fraz dla pyzy pochodząca z projektu android.

%prep
%setup -q
cp %{SOURCE1} data/db/open-phrase

%build
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

%files static
%defattr(644,root,root,755)
%{_libdir}/libpyzy-1.0.a

%files db-open-phrase
%defattr(644,root,root,755)
%{_datadir}/pyzy/db/open-phrase.db

%files db-android
%defattr(644,root,root,755)
%{_datadir}/pyzy/db/android.db
