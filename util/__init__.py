# -*- coding:utf-8 -*-

def getFileSizeString(sizeInBytes):
    """
    Convert the given byteCount into a string like: 9.9bytes/KB/MB/GB
    """
    for (cutoff, label) in [(1024*1024*1024, "GB"),
                            (1024*1024, "MB"),
                            (1024, "KB"),
                            ]:
        if sizeInBytes >= cutoff:
            return "%.1f %s" % (sizeInBytes * 1.0 / cutoff, label)

    if sizeInBytes == 1:
        return "1 byte"
    else:
        byte_str = "%.1f" % (sizeInBytes or 0,)
        return (byte_str[:-2] if byte_str.endswith('.0') else byte_str) + ' bytes'
    
if __name__ == "__main__":
    print getFileSizeString(189077245)
    print getFileSizeString(1718)
    print getFileSizeString(85)
    print getFileSizeString(185)
    