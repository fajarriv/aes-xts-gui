

from Crypto.Cipher import AES


class AESXTS:
    def __init__(self, key, tweak_input=b"\xff"*16):
        # block size = 16bytes = 128 bit, key = 32 bytehex= 256 bit
        self.block_size = 16
        self.key1 = key[:self.block_size]
        self.key2 = key[self.block_size:]
        self.i = tweak_input

        self.aes = AES.new(self.key1, AES.MODE_ECB)
        self.tweak = AES.new(self.key2, AES.MODE_ECB).encrypt(self.i)

    def encrypt(self, plaintext):
        tweak = self.tweak
        input_blocks = [plaintext[i: i+self.block_size]
                        for i in range(0, len(plaintext), self.block_size)]

        resultList = list()
        is_last_block_full = True  # flag to check if the last block is null
        # process encode until the second last block
        for current_block in input_blocks:

            if len(current_block) < self.block_size:
                is_last_block_full = False
                break

            # xor tweak with plaintext then AES encrypt
            cipher_block = self.aes.encrypt(
                self.block_xor(current_block, tweak))

            # xor cipher_block(aes encrypt result) with tweak then append to result list
            resultList.append(self.block_xor(cipher_block, tweak))

            # get next tweak
            tweak = self.get_next_tweak(tweak)

        # perform cipher text stealing for the last block if it is not full
        # Based on slide 33
        if (not is_last_block_full):
            partial_block_m = input_blocks[-1]
            # pop needed to 'swap' the order of the last two blocks
            xx = resultList.pop(-1)
            cp = xx[len(partial_block_m):]
            cm = xx[:len(partial_block_m)]

            yy = partial_block_m + cp

            # xor tweak (already last tweak) with plaintext then AES encrypt
            last_cipher_block = self.aes.encrypt(
                self.block_xor(yy, tweak))
            last_cipher_result = self.block_xor(last_cipher_block, tweak)

            resultList.append(last_cipher_result)
            resultList.append(cm)

        return b"".join(resultList)

    def decrypt(self, ciphertext):
        tweak = self.tweak
        input_blocks = [ciphertext[i: i+self.block_size]
                        for i in range(0, len(ciphertext), self.block_size)]

        resultPlain = list()

        is_last_block_full = len(input_blocks[-1]) == self.block_size

        # Normal xts aes block decryption
        if is_last_block_full:
            for current_block in input_blocks:
                # xor tweak with plaintext then AES decrypt
                plain_block = self.aes.decrypt(
                    self.block_xor(current_block, tweak))

                # xor plain_block(aes decrypt result) with tweak then append to result list
                resultPlain.append(self.block_xor(plain_block, tweak))
                # get next tweak
                tweak = self.get_next_tweak(tweak)

        # perform cipher-text stealing
        else:
            # process decode until the second last block
            for i in range(len(input_blocks)-2):
                current_block = input_blocks[i]

                # xor tweak with plaintext then AES decrypt
                plain_block = self.aes.decrypt(
                    self.block_xor(current_block, tweak))

                # xor plain_block(aes decrypt result) with tweak then append to result list
                resultPlain.append(self.block_xor(plain_block, tweak))
                # get next tweak
                tweak = self.get_next_tweak(tweak)

            # last_tweak/m-1 tweak for last block. tweak for the second last block
            last_tweak = tweak
            tweak = self.get_next_tweak(last_tweak)

            # second last block decrpytion
            plain_block = self.aes.decrypt(
                self.block_xor(input_blocks[-2], tweak))
            yy = self.block_xor(plain_block, tweak)

            cm = input_blocks[-1]
            pm = yy[:len(cm)]
            cp = yy[len(cm):]
            xx = cm + cp

            # last block decryption
            last_plain_block = self.aes.decrypt(self.block_xor(xx, last_tweak))
            last_plain_result = self.block_xor(last_plain_block, last_tweak)

            resultPlain.append(last_plain_result)
            resultPlain.append(pm)

        return b"".join(resultPlain)

    def block_xor(self, block1, block2):
        return bytes(b1 ^ b2 for b1, b2 in zip(block1, block2))

    def get_next_tweak(self, tweak):
        next_tweak = bytearray()
        carry_in = 0
        carry_out = 0
        for j in range(0, self.block_size):
            carry_out = (tweak[j] >> 7) & 1
            next_tweak.append(((tweak[j] << 1) + carry_in) & 0xFF)
            carry_in = carry_out
        if carry_out:
            next_tweak[0] ^= 0x87
        return next_tweak

# print(AES.block_size)
