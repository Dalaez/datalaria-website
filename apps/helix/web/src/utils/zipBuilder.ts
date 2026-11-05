/**
 * Empaquetador PKZIP determinista en TypeScript puro (cero dependencias externas).
 * Cumple con INV-HELIX-6: generación client-side en memoria del navegador.
 */

const makeCrcTable = (): Uint32Array => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) {
      c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    }
    table[n] = c >>> 0;
  }
  return table;
};

const crcTable = makeCrcTable();

const calcCrc32 = (data: Uint8Array): number => {
  let crc = 0 ^ -1;
  for (let i = 0; i < data.length; i++) {
    crc = (crc >>> 8) ^ crcTable[(crc ^ data[i]) & 0xff];
  }
  return (crc ^ -1) >>> 0;
};

export interface VirtualFile {
  name: string;
  content: string;
}

export function createZipBlob(files: VirtualFile[]): Blob {
  const encoder = new TextEncoder();
  const fileEntries = files.map((f) => {
    const nameBytes = encoder.encode(f.name.replace(/\\/g, '/'));
    const dataBytes = encoder.encode(f.content);
    const crc = calcCrc32(dataBytes);
    return {
      name: f.name,
      nameBytes,
      dataBytes,
      crc,
      size: dataBytes.length,
      offset: 0,
    };
  });

  // Calcular tamaño total
  let localHeadersSize = 0;
  let centralDirSize = 0;

  for (const entry of fileEntries) {
    localHeadersSize += 30 + entry.nameBytes.length + entry.size;
    centralDirSize += 46 + entry.nameBytes.length;
  }

  const totalSize = localHeadersSize + centralDirSize + 22;
  const buffer = new ArrayBuffer(totalSize);
  const view = new DataView(buffer);
  const bytes = new Uint8Array(buffer);

  let currentOffset = 0;

  // 1. Escribir Local File Headers y Datos
  for (const entry of fileEntries) {
    entry.offset = currentOffset;

    // Local file header signature (0x04034b50)
    view.setUint32(currentOffset, 0x04034b50, true);
    view.setUint16(currentOffset + 4, 20, true); // Versión necesaria
    view.setUint16(currentOffset + 6, 0x0800, true); // UTF-8 flag
    view.setUint16(currentOffset + 8, 0, true); // Método 0: STORE
    view.setUint16(currentOffset + 10, 0, true); // Hora dos
    view.setUint16(currentOffset + 12, 0, true); // Fecha dos
    view.setUint32(currentOffset + 14, entry.crc, true); // CRC-32
    view.setUint32(currentOffset + 18, entry.size, true); // Compressed size
    view.setUint32(currentOffset + 22, entry.size, true); // Uncompressed size
    view.setUint16(currentOffset + 26, entry.nameBytes.length, true);
    view.setUint16(currentOffset + 28, 0, true); // Extra field length

    currentOffset += 30;
    bytes.set(entry.nameBytes, currentOffset);
    currentOffset += entry.nameBytes.length;

    bytes.set(entry.dataBytes, currentOffset);
    currentOffset += entry.size;
  }

  const centralDirStart = currentOffset;

  // 2. Escribir Central Directory Headers
  for (const entry of fileEntries) {
    // Central directory header signature (0x02014b50)
    view.setUint32(currentOffset, 0x02014b50, true);
    view.setUint16(currentOffset + 4, 20, true); // Versión hecha por
    view.setUint16(currentOffset + 6, 20, true); // Versión necesaria
    view.setUint16(currentOffset + 8, 0x0800, true); // UTF-8 flag
    view.setUint16(currentOffset + 10, 0, true); // Método 0: STORE
    view.setUint16(currentOffset + 12, 0, true); // Hora dos
    view.setUint16(currentOffset + 14, 0, true); // Fecha dos
    view.setUint32(currentOffset + 16, entry.crc, true);
    view.setUint32(currentOffset + 20, entry.size, true);
    view.setUint32(currentOffset + 24, entry.size, true);
    view.setUint16(currentOffset + 28, entry.nameBytes.length, true);
    view.setUint16(currentOffset + 30, 0, true); // Extra field
    view.setUint16(currentOffset + 32, 0, true); // Comment length
    view.setUint16(currentOffset + 34, 0, true); // Disk start
    view.setUint16(currentOffset + 36, 0, true); // Internal attributes
    view.setUint32(currentOffset + 38, 0, true); // External attributes
    view.setUint32(currentOffset + 42, entry.offset, true); // Local header offset

    currentOffset += 46;
    bytes.set(entry.nameBytes, currentOffset);
    currentOffset += entry.nameBytes.length;
  }

  // 3. Escribir End of Central Directory Record (0x06054b50)
  view.setUint32(currentOffset, 0x06054b50, true);
  view.setUint16(currentOffset + 4, 0, true); // Disk number
  view.setUint16(currentOffset + 6, 0, true); // Central dir disk
  view.setUint16(currentOffset + 8, fileEntries.length, true); // Total entries disk
  view.setUint16(currentOffset + 10, fileEntries.length, true); // Total entries
  view.setUint32(currentOffset + 12, centralDirSize, true); // Central dir size
  view.setUint32(currentOffset + 16, centralDirStart, true); // Central dir offset
  view.setUint16(currentOffset + 20, 0, true); // Comment length

  return new Blob([buffer], { type: 'application/zip' });
}

export function downloadZip(filename: string, files: VirtualFile[]): void {
  const blob = createZipBlob(files);
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
