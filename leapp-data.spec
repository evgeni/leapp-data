Name:		leapp-data
Version:	0.4
Release:	1%{?dist}
Summary:	data for leapp
License:	ASL 2.0
URL:		https://github.com/evgeni/leapp-data
BuildArch:  noarch
Source0: %{name}-%{version}.tar.gz

%description
%{summary}


%prep
%setup -q


%build

%{lua:
distros = {'almalinux', 'centos', 'eurolinux', 'ol', 'rocky'}

print('%install\n')
for _, distro in ipairs(distros) do
  print('install -D -m0644 -T ' .. distro .. '/leapp_upgrade_repositories.repo' .. ' ' .. rpm.expand('%{buildroot}') .. '/etc/leapp/files/leapp_upgrade_repositories.repo.' .. distro .. '\n')
  if distro ~= 'centos' then
    print('install -D -m0644 -T ' .. distro .. '/gpg-signatures.json'.. ' ' .. rpm.expand('%{buildroot}') .. '/usr/share/leapp-repository/repositories/system_upgrade/common/files/distro/' .. distro .. '/gpg-signatures.json\n')
  end
end

for _, distro in ipairs(distros) do
  print('%package -n leapp-data-' .. distro .. '\n')
  print('Summary: leapp data for ' .. distro.. '\n')
  print('RemovePathPostfixes: .' .. distro .. '\n')
  for _, other_distro in ipairs(distros) do
    if distro ~= other_distro then
      print('Conflicts: leapp-data-' .. other_distro .. '\n')
    end
  end

  print('%description -n leapp-data-' .. distro.. '\n')
  print('leapp data for ' .. distro.. '\n')

  print('%files ' .. distro.. '\n')
  print('/etc/leapp/files/*' .. distro.. '\n')
  if distro ~= 'centos' then
    print('/usr/share/leapp-repository/repositories/system_upgrade/common/files/distro/' .. distro.. '\n')
  end
end
}

%changelog
* Tue Aug 20 2024 Evgeni Golov - 0.4-1
- Add obsoleted GPG keys for Almalinux

* Tue Jun 11 2024 Evgeni Golov - 0.3-1
- Rewrite package to generate all RPMS from one SRPM using Lua
- Only ship repositories and GPG data, everything else is in leapp-repository already
- Drop EL8 data
- Only include BaseOS and AppStream repos by default
