  program readHYDRO
! Extract part of HYDRO1K data file knowing coordinates used (i.e. km).
!
! DBC 04/11/04 Minor changes, including getting min and max.
!
! v1.1 DBC 23/10/03
!    Gets all fields in one run..even aspect which seems to be wrong, and is anyway easily derived.
!
! DBC 23/10/03
!------------------------------------------------------------------------
!2345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678_132
     
  implicit none

  integer, parameter ::  &
    inUnit = 1    &!  unit used for input
   ,nvar = 6      &!  number of variables (z,area,slope,topo index,flow dir, aspect)
   ,nxmax = 8319  &!  x extent of input data files
   ,nymax = 7638  &!  y extent of input data files
   ,outUnit=11     !  unit used for output

  integer, parameter ::  &!  ARRAYS
    reclIn(nvar) = (/ 2,4,2,2,2,2 /)   !  record lengths (for a single value) for input files

  integer :: irec,irecOut=0  &
    ,ival       &!  a value read in (from 32-bit input file)
    ,ivar       &!
    ,ix         &
    ,ix1,ix2    &!  indices (in full grid) of left and right edge points respectively
    ,iy         &
    ,iy1,iy2    &!  indices (in full grid) of bottom and top edge points respectively
    ,nx,ny       !  extents of area selected

  integer*2 :: &!   I don't know how to ensure 16-bit data can be read with selected_int_kind!
    ival2       !   a value read from 16-bit input file

  real, parameter ::  &
    dx = 1000.0   &!  size of input gridbox (m)
   ,mult(nvar) = (/ 1.0, 1.0, 0.01, 0.01, 1.0, 0.01 /)  &!  multiplier to change units of variables (see readme.eu)
!    The following distances refer to the projection of the input data.
   ,xlhsCentre=-4091.0e3  &!  x-projected location of centre of leftmost pixel of input grid (m)
!                          !   (really at top left of image)
   ,ytopCentre=3293.0e3    !  y-projected location of centre of leftmost pixel of input grid (m)
!                          !   (really at top left of image)

  real ::  &
    rval   &!  final value of a datum, as written out
!   The following distances refer to the projection of the input data.
   ,x1,x2,y1,y2   ! projected distances to outside of chosen area (m)

  real :: minmax(nvar,2)  !  min and max value found for each variable

  character(len=100) :: outctl,outgra

  character(len=100), parameter ::  &
! NB These character array constructors must all be of same length.
    infile(nvar) = (/   &!  input files
         '/users/global/dbcl/data/gtopo30/hydro1k/orig/eu_dem.bil  '  &
        ,'/users/global/dbcl/data/gtopo30/hydro1k/orig/eu_fa.bil   '  &
        ,'/users/global/dbcl/data/gtopo30/hydro1k/orig/eu_slope.bil'  &
        ,'/users/global/dbcl/data/gtopo30/hydro1k/orig/eu_cti.bil  '  &
        ,'/users/global/dbcl/data/gtopo30/hydro1k/orig/eu_fd.bil   '  &
        ,'/users/global/dbcl/data/gtopo30/hydro1k/orig/eu_asp.bil  ' /)  &
   ,varline(nvar) = (/  &!  lines used for each variable in output ctl file
      'z    0 99  elevation (m)                                         ' &
     ,'area 0 99  area draining to point (km2)                          ' &
     ,'s    0 99  (max) slope (degrees)                                 ' &
     ,'ti   0 99  topographic index                                     ' &
     ,'fd   0 99  flow direction (coded, 1-128 clockwise from E)        ' &
     ,'as   0 99  aspect (0 to 360 degrees from N - seems to be rubbish)'  /)

!------------------------------------------------------------------------------------------------
! Set up varline. (If done at declaration, all values must have same length.)
!------------------------------------------------------------------------------------------------

! Specify area to be extracted. These coords should be the outside of the area.
!  x1=-1290.0e3; x2=-1210.0e3  !  Ardeche
!  y1=-1067.0e3; y2=-990.0e3
! Specify output file name.
!  outgra = '/users/global/dbcl/data/gtopo30/hydro1k/work/ardeche_1km.gra'

! Specify area to be extracted. These coords should be the outside of the area.
!  x1=-1080.0e3; x2=-1015.0e3  !  Durance
!  y1=-1070.0e3; y2=-995.0e3
! Specify output file name.
!  outgra = '/users/global/dbcl/data/gtopo30/hydro1k/work/durance_1km.gra'

! Specify area to be extracted. These coords should be the outside of the area.
!  x1=-1100.0e3; x2=-1045.0e3  !  Ain
!  y1=-848.0e3; y2=-795.0e3
! Specify output file name.
!  outgra = '/users/global/dbcl/data/gtopo30/hydro1k/work/ain_1km.gra'

! Specify area to be extracted. These coords should be the outside of the area.
!  x1=-1090.0e3; x2=-975.0e3  !  Ognon
!  y1=-765.0e3; y2=-695.0e3
! Specify output file name.
!  outgra = '/users/global/dbcl/data/gtopo30/hydro1k/work/ognon_1km.gra'

! Specify area to be extracted. These coords should be the outside of the area.
!  x1=-1180.0e3; x2=-970.0e3  !  Saone at Le Chatelet
!  y1=-780.0e3; y2=-650.0e3
! Specify output file name.
!  outgra = '/users/global/dbcl/data/gtopo30/hydro1k/work/saone_1km.gra'

! Specify area to be extracted. These coords should be the outside of the area.
  x1=-20000.0e3; x2=20000.0e3  !  entire area, made-up coords that default to whole grid
  y1=-20000.0e3; y2=20000.0e3
! Specify output file name.
  outgra = '/scratch/dbcl/eu_1km.gra'

! Get outctl assuming outgra ends with gra!
  ix = len_trim( outgra ) - 3
  outctl = outgra(1:ix) // 'ctl'

! Locate this area in the grid.
! Note the input is arraned N to S. These row numbers (iy) are for S to N order (as output).
! Use nint, which may mean that actual area will be slightly more or less than requested.
  ix1 = nint( (x1-xlhsCentre-0.5*dx)/dx )   !  allowing for small difference between centre of pixel and edge
  ix2 = nint( (x2-xlhsCentre-0.5*dx)/dx )
  iy1 = nyMax - nint( (ytopCentre+0.5*dx-y1)/dx ) + 1
  iy2 = nyMax - nint( (ytopCentre+0.5*dx-y2)/dx ) + 1

  ix1 = max( ix1, 1 )
  ix2 = min( ix2, nxMax )
  iy1 = max( iy1, 1 )
  iy2 = min( iy2, nyMax )
  nx = ix2 - ix1 + 1
  ny = iy2 - iy1 + 1

  write(*,*)'Area output represents nx=',nx,' ny=',ny
  write(*,*)'This is ix=',ix1,' to ',ix2,' iy=',iy1,' to ',iy2

! Intialise min and max.
  minmax(:,1) = 1.0e20
  minmax(:,2) = -1.0e20

! Open the output file.
  open(outUnit,file=outgra,form='unformatted',access='direct',recl=4,action='write',status='new')

! Loop over variables.
  do ivar=1,nvar

    write(*,*)'Doing var #',ivar,' mult=',mult(ivar),' reclIn=',reclIn(ivar)
    write(*,*) trim(infile(ivar))

!   Read and write one value at a time - which likely isn't very efficient for large areas.
    open(inUnit,file=infile(ivar),form='unformatted',access='direct',recl=reclIn(ivar),action='read',status='old')

    do iy=iy1,iy2
      if ( mod(iy-iy1+1,500) == 0 ) then
        write(*,*) 'Reading row #',iy-iy1+1,' of ',ny
        write(*,*) 'Current min and max=',minmax(ivar,:)
      endif
      do ix=ix1,ix2
        irec = (nyMax-iy)*nxMax + ix   !  convert to read S to N
        if ( reclIn(ivar)==2 ) then
          read(inUnit,rec=irec) ival2
          ival = int( ival2 )
        else
          read(inUnit,rec=irec) ival
        endif
        irecOut = irecOut + 1
        rval = real( ival ) * mult(ivar)
        write(outUnit,rec=irecOut) rval
        if ( rval < minmax(ivar,1) ) minmax(ivar,1)=rval
        if ( rval > minmax(ivar,2) ) minmax(ivar,2)=rval
      enddo
    enddo

    close(inUnit)

  enddo  !  ivar

  close(outUnit)

! Write a GrADS ctl file.
  open(outUnit,file=outctl,action='write',status='replace')   !  NB replacing
  write(outUnit,"('dset ',a)") trim(outgra)
  write(outUnit,"('options big_endian')")
  write(outUnit,"('title Data from HYDRO1K, written by hydro1k_extract_v1.f90')")
  write(outUnit,"('undef -9999.0')") 
  write(outUnit,"('* Note made up x,y coords. This is 1km data.')") 
  write(outUnit,"('xdef ',i5,' linear 0.0 0.008333')") nx 
  write(outUnit,"('ydef ',i5,' linear 0.0 0.008333')") ny
  write(outUnit,"('zdef 1 linear 1 1')") 
  write(outUnit,"('tdef 1 linear 00Z01AUG1985 3hr')")
  write(outUnit,"('vars ',i2)") nvar
  do ivar=1,nvar
    write(outUnit,"(a)") trim(varline(ivar))
  enddo
  write(outUnit,"('endvars')") 

! Print min and max values.
  write(*,"(/,a)") 'Min and max values (including multiplier):'
  do ivar=1,nvar
    write(*,*) varline(ivar)(1:4),minmax(ivar,:)
  enddo

  write(*,*)'Output was to ',trim(outgra)

  end program readHYDRO

