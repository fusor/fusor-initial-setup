#!/bin/bash

TMP_DIR=/tmp/foreman-discovery-image-repair
BOOT_DIR=/var/lib/tftpboot/boot
ISO_PATH=`ls /usr/share/foreman-discovery-image/foreman-discovery-image-*.iso`
ISO_FILE=`basename ${ISO_PATH}`
FDI_VMLINUZ="fdi-image-rhel_7-vmlinuz"
FDI_IMG="fdi-image-rhel_7-img"


mkdir -p ${TMP_DIR}
cd ${TMP_DIR}

ln -snf ${ISO_PATH} fdi.iso
livecd-iso-to-pxeboot fdi.iso

cp ${TMP_DIR}/tftpboot/initrd0.img  ${BOOT_DIR}/${ISO_FILE}-img
cp ${TMP_DIR}/tftpboot/vmlinuz0 ${BOOT_DIR}/${ISO_FILE}-vmlinuz

cd ${BOOT_DIR}
rm -f ${FDI_VMLINUZ}
rm -f ${FDI_IMG}
ln -s ${ISO_FILE}-vmlinuz ${FDI_VMLINUZ}
ln -s ${ISO_FILE}-img ${FDI_IMG}

restorecon -R ${BOOT_DIR}
chown -R foreman-proxy:root ${BOOT_DIR}/*

rm -rf ${TMP_DIR}


