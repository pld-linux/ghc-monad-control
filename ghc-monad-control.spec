#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	monad-control
Summary:	Generic control operations
Summary(pl.UTF-8):	Ogólne operacje sterujące
Name:		ghc-%{pkgname}
Version:	1.0.2.3
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/monad-control
Source0:	http://hackage.haskell.org/package/monad-control-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	4b7ba1532ac949818947d08f2aa88d0c
URL:		http://hackage.haskell.org/package/monad-control
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-base-unicode-symbols >= 0.1.1
BuildRequires:	ghc-transformers >= 0.2
BuildRequires:	ghc-transformers-base >= 0.4.1
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-base-unicode-symbols-prof >= 0.1.1
BuildRequires:	ghc-transformers-prof >= 0.2
BuildRequires:	ghc-transformers-base-prof >= 0.4.1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 3
Requires:	ghc-base-unicode-symbols >= 0.1.1
Requires:	ghc-transformers >= 0.2
Requires:	ghc-transformers-base >= 0.4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
This package defines the type class MonadBaseControl, a subset of
MonadBase into which generic control operations such as catch can be
lifted from IO or any other base monad. Instances are based on monad
transformers in MonadTransControl, which includes all standard monad
transformers in the transformers library except ContT.

%description -l pl.UTF-8
Ten pakiet definiuje klasę typu MonadBaseControl, będącą podzbiorem
MonadBase, do której można podnieść ogólne operacje sterujące (takie
jak catch) z IO lub dowolnej innej podstawowej monady. Instancje są
oparte na transformatorach monad w MonadTransControl, która dołącza
wszystkie standardowe transformatory monad z biblioteki transformers z
wyjątkiem ContT.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3
Requires:	ghc-base-unicode-symbols-prof >= 0.1.1
Requires:	ghc-transformers-prof >= 0.2
Requires:	ghc-transformers-base-prof >= 0.4.1

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README.markdown
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSmonad-control-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSmonad-control-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSmonad-control-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Control.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Control.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSmonad-control-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Control.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
