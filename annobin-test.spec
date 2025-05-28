Name: annobin-test
Version: 1.0.0
Release: %autorelease
Summary: A "Hello, world!" program build with gcc and clang

License: BSD-3-Clause
URL: http://www.example.com
Source0: welcome.c
Source1: print_welcome.h
Source2: print_welcome.c

BuildRequires: clang
BuildRequires: gcc
BuildRequires: annobin-plugin-clang
BuildRequires: annobin-plugin-llvm
BuildRequires: annobin-plugin-gcc
BuildRequires: annobin-annocheck

%description
This package contains "Hello, world!" binaries built with gcc
and clang. The binaries are annotated.

%prep
rm -rf out
mkdir -pv out

%build

#region build-with-gcc

%global extra_flags_gcc %nil

# Hardened: main-gcc: FAIL: bind-now test because not linked with -Wl,-z,now
# See https://sourceware.org/annobin/annobin.html/Test-bind-now.html
%global extra_flags_gcc %{?extra_flags_gcc} -Wl,-z,now

# Hardened: main-gcc: FAIL: pie test because not built with '-Wl,-pie' 
# See https://sourceware.org/annobin/annobin.html/Test-pic.html
%global extra_flags_gcc %{?extra_flags_gcc} -fPIC

# Hardened: main-gcc: FAIL: cf-protection test because no .note.gnu.property section = no control flow information 
# See https://sourceware.org/annobin/annobin.html/Test-cf-protection.html
%global extra_flags_gcc %{?extra_flags_gcc} -fcf-protection=full

# Build *.so
gcc -shared -o out/libprint_welcome-gcc.so %{?extra_flags_gcc} %{SOURCE2}

gcc -o out/main-gcc -Lout/ -lprint_welcome-gcc %{?extra_flags_gcc} %{SOURCE0}

#endregion build-with-gcc

#endregion build-with-clang

%global extra_flags_clang %nil

# Hardened: main-clang: FAIL: bind-now test because not linked with -Wl,-z,now 
# See https://sourceware.org/annobin/annobin.html/Test-bind-now.html
%global extra_flags_clang %{?extra_flags_clang} -Wl,-z,now

# Hardened: main-clang: FAIL: cf-protection test because no .note.gnu.property section = no control flow information 
# See https://sourceware.org/annobin/annobin.html/Test-cf-protection.html
%global extra_flags_clang %{?extra_flags_clang} -fcf-protection=full

# Build *.so
clang -shared -o out/libprint_welcome-clang.so %{?extra_flags_clang} %{SOURCE2}

clang -o out/main-clang -Lout/ -lprint_welcome-clang %{?extra_flags_clang} %{SOURCE0}

#endregion build-with-clang

%install
mkdir -pv %{buildroot}%{_bindir}
mkdir -pv %{buildroot}%{_libdir}

install out/main-gcc %{buildroot}%{_bindir}/welcome_gcc
install out/main-clang %{buildroot}%{_bindir}/welcome_clang
install out/libprint_welcome-gcc.so %{buildroot}%{_libdir}/libprint_welcome-gcc.so
install out/libprint_welcome-clang.so %{buildroot}%{_libdir}/libprint_welcome-clang.so

%check
# Check each binary outputs its compiler
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}

[[ "`%{buildroot}%{_bindir}/welcome_gcc`" != "Hello, world! (gcc)" ]] && exit 111;
[[ "`%{buildroot}%{_bindir}/welcome_clang`" != "Hello, world! (clang)" ]] && exit 222;

# NOTE: I know that annocheck can check the whole RPM later but
# I want to also test the binaries and shared objects here
# individually to see what things I need to tweak for what artifact.

# Hardened: main-gcc: FAIL: pie test because not built with '-Wl,-pie' 
# See https://sourceware.org/annobin/annobin.html/Test-pie.html 
annocheck --skip-pie %{buildroot}%{_bindir}/welcome_gcc
annocheck --verbose %{buildroot}%{_libdir}/libprint_welcome-gcc.so

# Hardened: main-clang: FAIL: pie test because not built with '-Wl,-pie' 
# See https://sourceware.org/annobin/annobin.html/Test-pie.html 
annocheck --skip-pie %{buildroot}%{_bindir}/welcome_clang
annocheck --skip-pie %{buildroot}%{_libdir}/libprint_welcome-clang.so

%files
%{_bindir}/welcome_gcc
%{_bindir}/welcome_clang
%{_libdir}/libprint_welcome-gcc.so
%{_libdir}/libprint_welcome-clang.so

%changelog
%autochangelog