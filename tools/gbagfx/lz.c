// Copyright (c) 2015 YamaArashi

#include <stdlib.h>
#include <stdbool.h>
#include "global.h"
#include "lz.h"

unsigned char *LZDecompress(unsigned char *src, int srcSize, int *uncompressedSize)
{
	if (srcSize < 4)
		goto fail;

	int destSize = (src[3] << 16) | (src[2] << 8) | src[1];

	unsigned char *dest = malloc(destSize);

	if (dest == NULL)
		goto fail;

	int srcPos = 4;
	int destPos = 0;

	for (;;) {
		if (srcPos >= srcSize)
			goto fail;

		unsigned char flags = src[srcPos++];

		for (int i = 0; i < 8; i++) {
			if (flags & 0x80) {
				if (srcPos + 1 >= srcSize)
					goto fail;

				int blockSize = (src[srcPos] >> 4) + 3;
				int blockDistance = (((src[srcPos] & 0xF) << 8) | src[srcPos + 1]) + 1;

				srcPos += 2;

				int blockPos = destPos - blockDistance;

				// Some Ruby/Sapphire tilesets overflow.
				if (destPos + blockSize > destSize) {
					blockSize = destSize - destPos;
					fprintf(stderr, "Destination buffer overflow.\n");
				}

				if (blockPos < 0)
					goto fail;

				for (int j = 0; j < blockSize; j++)
					dest[destPos++] = dest[blockPos + j];
			} else {
				if (srcPos >= srcSize || destPos >= destSize)
					goto fail;

				dest[destPos++] = src[srcPos++];
			}

			if (destPos == destSize) {
				*uncompressedSize = destSize;
				return dest;
			}

			flags <<= 1;
		}
	}

fail:
	FATAL_ERROR("Fatal error while decompressing LZ file.\n");
}

// Project Grounded (v0.9.229): optimale parse i.p.v. greedy. Zelfde formaat (de GBA pakt het identiek uit);
// per positie de langste match (elke kortere lengte kan met dezelfde afstand), dan van achter naar voren het minste
// aantal bits (literal 9, match 17).
unsigned char *LZCompress(unsigned char *src, int srcSize, int *compressedSize, const int minDistance)
{
	if (srcSize <= 0)
		goto fail;

	int worstCaseDestSize = 4 + srcSize + ((srcSize + 7) / 8);

	// Round up to the next multiple of four.
	worstCaseDestSize = (worstCaseDestSize + 3) & ~3;

	unsigned char *dest = malloc(worstCaseDestSize);
	int *matchLen = malloc(sizeof(int) * srcSize);
	int *matchDist = malloc(sizeof(int) * srcSize);
	int *cost = malloc(sizeof(int) * (srcSize + 1));
	int *choice = malloc(sizeof(int) * srcSize);

	if (dest == NULL || matchLen == NULL || matchDist == NULL || cost == NULL || choice == NULL)
		goto fail;

	for (int pos = 0; pos < srcSize; pos++) {
		int bestBlockDistance = 0;
		int bestBlockSize = 0;
		for (int blockDistance = minDistance; blockDistance <= pos && blockDistance <= 0x1000; blockDistance++) {
			int blockStart = pos - blockDistance;
			int blockSize = 0;
			while (blockSize < 18
			    && pos + blockSize < srcSize
			    && src[blockStart + blockSize] == src[pos + blockSize])
				blockSize++;
			if (blockSize > bestBlockSize) {
				bestBlockDistance = blockDistance;
				bestBlockSize = blockSize;
				if (blockSize == 18)
					break;
			}
		}
		matchLen[pos] = bestBlockSize;
		matchDist[pos] = bestBlockDistance;
	}

	cost[srcSize] = 0;
	for (int pos = srcSize - 1; pos >= 0; pos--) {
		cost[pos] = 9 + cost[pos + 1];
		choice[pos] = 1;
		for (int len = 3; len <= matchLen[pos]; len++) {
			if (17 + cost[pos + len] < cost[pos]) {
				cost[pos] = 17 + cost[pos + len];
				choice[pos] = len;
			}
		}
	}

	// header
	dest[0] = 0x10; // LZ compression type
	dest[1] = (unsigned char)srcSize;
	dest[2] = (unsigned char)(srcSize >> 8);
	dest[3] = (unsigned char)(srcSize >> 16);

	int srcPos = 0;
	int destPos = 4;

	for (;;) {
		unsigned char *flags = &dest[destPos++];
		*flags = 0;

		for (int i = 0; i < 8; i++) {
			int len = choice[srcPos];
			if (len >= 3) {
				int dist = matchDist[srcPos] - 1;
				*flags |= (0x80 >> i);
				dest[destPos++] = ((len - 3) << 4) | ((unsigned int)dist >> 8);
				dest[destPos++] = (unsigned char)dist;
				srcPos += len;
			} else {
				dest[destPos++] = src[srcPos++];
			}

			if (srcPos == srcSize) {
				// Pad to multiple of 4 bytes.
				int remainder = destPos % 4;

				if (remainder != 0) {
					for (int i = 0; i < 4 - remainder; i++)
						dest[destPos++] = 0;
				}

				free(matchLen);
				free(matchDist);
				free(cost);
				free(choice);
				*compressedSize = destPos;
				return dest;
			}
		}
	}

fail:
	FATAL_ERROR("Fatal error while compressing LZ file.\n");
}
