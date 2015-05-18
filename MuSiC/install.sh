#! /bin/bash

die () {
  echo "$@"
  exit 1
}

APT_URL=http://apt.genome.wustl.edu/ubuntu
KEY_URL=http://apt.genome.wustl.edu/ubuntu/files/genome-institute.asc
DIST=lucid-genome
APT_LIST=/etc/apt/sources.list.d/genome.list

if ! lsb_release -c 2>/dev/null | grep -q lucid; then
  die "This host is not running Ubuntu 10.04"
fi

PKG=genome
[ -n "$PKG" ] || \
  die "Please specify the package to install (eg. genome-music)."

[ -d /etc/apt/sources.list.d ] || \
  die "/etc/apt/sources.list.d is not a directory. It looks like this host does not use apt."

APT_PREF="\
# $DIST
Package: *
Pin: release n=$DIST
Pin-Priority: 990"
APT_PREF_FILE="/etc/apt/preferences.d/$DIST.pref"
echo "$APT_PREF" > "$APT_PREF_FILE"

LINE="deb $APT_URL $DIST main"
grep -q "$LINE" "$APT_LIST" 2>/dev/null || \
{
  echo "Adding Genome Institute apt repository to $APT_LIST"
  cat > $APT_LIST <<EOF || die "Cannot write to $APT_LIST."
$LINE
EOF
}

apt-key list 2>/dev/null | grep -q "codesigner@genome.wustl.edu" || \
{
  echo "Adding Genome Institute apt key to keyring"
  wget -q -O - 2>/dev/null $KEY_URL | \
    apt-key add - >/dev/null 2>&1 || \
    die "There was an error importing GPG key with apt-key."
  echo Success
}

apt-get -q2 update || \
  die "There was an error running apt-get update."

echo "Installing $PKG..."
apt-get -y install "$PKG" || \
  die "There was an error installing $PKG."

echo "Success!"
echo "To install genome modules, now run:"
echo "genome install --yes \$MODULENAME"
