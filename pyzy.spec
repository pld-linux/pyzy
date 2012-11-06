Summary:	The Chinese PinYin and Bopomofo conversion library
Name:		pyzy
Version:	0.1.0
Release:	3
License:	LGPL v2.1
Group:		Libraries
Source0:	http://pyzy.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	73afc3c20808af2fee5f9fca47c64630
Source1:	http://pyzy.googlecode.com/files/%{name}-database-1.0.0.tar.bz2
# Source1-md5:	d0951b8daa7f56a2cbd3b6b4e42532e0
URL:		http://code.google.com/p/pyzy
BuildRequires:	boost-devel
BuildRequires:	glib2-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	opencc-devel
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel
Requires(post,postun):	/sbin/ldconfig
Suggests:	%{name}-db = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Chinese Pinyin and Bopomofo conversion library.

%package common
Summary:	Common files for pyzy and phrase databases
Group:		Libraries
BuildArch:	noarch

%description common
Common files for pyzy and phrase databases.

%package devel
Summary:	Development tools for pyzy
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel

%description devel
The pyzy-devel package contains the header files for pyzy.

%package db-open-phrase
Summary:	The open phrase database for pyzy
Group:		Libraries
Obsoletes:	ibus-pinyin-db-open-phrase < 1.4.99
Provides:	%{name}-db = %{version}-%{release}
Requires:	%{name}-common = %{version}-%{release}
BuildArch:	noarch

%description db-open-phrase
The phrase database for pyzy from open-phrase project.

%package db-android
Summary:	The android phrase database for pyzy
Group:		Libraries
Obsoletes:	ibus-pinyin-db-android < 1.4.99
Provides:	%{name}-db = %{version}-%{release}
Requires:	%{name}-common = %{version}-%{release}
BuildArch:	noarch

%description db-android
The phrase database for pyzy from android project.

%prep
%setup -q
cp %{SOURCE1} data/db/open-phrase

%build
%configure \
	--disable-static \
	--enable-boost \
	--enable-opencc \
	--enable-db-open-phrase

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.0

%files common
%defattr(644,root,root,755)
%dir %{_datadir}/pyzy
%dir %{_datadir}/pyzy/db
%{_datadir}/pyzy/phrases.txt
%{_datadir}/pyzy/db/create_index.sql

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_pkgconfigdir}/*
%{_includedir}/*

%files db-open-phrase
%defattr(644,root,root,755)
%{_datadir}/pyzy/db/open-phrase.db

%files db-android
%defattr(644,root,root,755)
%{_datadir}/pyzy/db/android.db
