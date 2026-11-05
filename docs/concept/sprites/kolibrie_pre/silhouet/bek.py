import math
def snavel(bx,by,hoek,L,dik,tip=0.25):
    """driehoekige snavelhelft: basis (bx,by), richting hoek (graden, 180=links, omhoog = >180 in beeld? we gebruiken wiskundig: y omlaag)"""
    r=math.radians(hoek); dx,dy=math.cos(r),-math.sin(r); nx,ny=-dy,dx
    tx,ty=bx+dx*L,by+dy*L
    return [(bx+nx*dik,by+ny*dik),(tx+nx*dik*tip,ty+ny*dik*tip),(tx-nx*dik*tip,ty-ny*dik*tip),(bx-nx*dik,by-ny*dik)]
def open_bek(bx,by,hoek,L,dik,open_=22):
    return [snavel(bx,by-dik*0.9,hoek+open_/2,L,dik), snavel(bx,by+dik*0.9,hoek-open_/2,L*0.88,dik)]
