# Example Code From Download Page Example

from lightkurve import search_targetpixelfile

pixelfile = search_targetpixelfile("KIC 8462852", quarter=16).download()

print("Downloaded pixel file successfully!")

lc = pixelfile.to_lightcurve(aperture_mask='all')

print(lc)
print("Number of data points:", len(lc.time))

lc.plot()

print("Test Done")