import openmc #type:ignore

openmc.config['cross_sections'] = ('/mnt/f/OpenMC/OpenMC_Data/endfb-viii.0-hdf5/cross_sections.xml')



#=======================
# Materials
#=======================

materials = openmc.Materials()

fuel = openmc.Material(name='U-ZrH TRIGA Fuel')
fuel.add_nuclide('U234', 0.00178, 'wo')
fuel.add_nuclide('U235', 0.17872, 'wo')
fuel.add_nuclide('U236', 0.00092, 'wo')
fuel.add_nuclide('U238', 0.81858, 'wo')
fuel.add_element('Zr', 1.0, 'wo')
fuel.add_element('H', 1.0, 'wo')
fuel.set_density('g/cm3', 8.26)
materials.append(fuel)

aluminium = openmc.Material(name='Aluminum Cladding')
aluminium.add_element('Al', 1.0)
aluminium.set_density('g/cm3', 2.7)
materials.append(aluminium)

graphite = openmc.Material(name='Graphite Reflector')
graphite.add_element('C', 1.0)
graphite.set_density('g/cm3', 1.76)
graphite.add_s_alpha_beta('c_Graphite')
materials.append(graphite)

water = openmc.Material(name='Light Water')
water.add_element('H', 2.0)
water.add_element('O', 1.0)
water.set_density('g/cm3', 1.0)
water.add_s_alpha_beta('c_H_in_H2O')
materials.append(water)



#=======================
# Geometry
#=======================

#Defining surfaces
fuel_radius = openmc.ZCylinder(r=1.76)
cladding_radius = openmc.ZCylinder(r=1.865)
fuel_top = openmc.ZPlane(z0=17.8)
fuel_bottom = openmc.ZPlane(z0=-17.8)
graphite_top = openmc.ZPlane(z0=36.12)
graphite_bottom = openmc.ZPlane(z0=-36.12)



#-----------------------
# Fuel Rod
#-----------------------

fuel_cell = openmc.Cell(
    name = 'Fuel',
    fill = fuel,
    region = +fuel_bottom & -fuel_top & -fuel_radius
)

graphite_rod_reflector_top = openmc.Cell(
    name = 'Graphite Rod Reflector Top',
    fill = graphite,
    region = -fuel_radius & -fuel_bottom & +graphite_bottom
)

graphite_rod_reflector_bottom = openmc.Cell(
    name = 'Graphite Rod Reflector Bottom',
    fill = graphite,
    region = -fuel_radius & -graphite_top & +fuel_top
)

cladding_cell = openmc.Cell(
    name = 'Cladding',
    fill = aluminium,
    region = +fuel_radius & -cladding_radius & +graphite_bottom & -graphite_top
)

water_cell = openmc.Cell(
    name = 'Water Moderator',
    fill = water,
    region = +cladding_radius & +graphite_bottom & -graphite_top
)

water_top = openmc.Cell(
    name = 'Water Top',
    fill = water,
    region = +graphite_top 
)

water_bottom = openmc.Cell(
    name = 'Water Bottom',
    fill = water,
    region = -graphite_bottom
)


pin_universe = openmc.Universe(
    name = 'Fuel Pin',
    cells = [
        fuel_cell,
        graphite_rod_reflector_top,
        graphite_rod_reflector_bottom,
        cladding_cell,
        water_cell,
        water_top,
        water_bottom
    ]
)


#-----------------------
# Lattice
#-----------------------

lattice = openmc.HexLattice(name='Core Lattice')
lattice.center = (0.0, 0.0)
lattice.pitch = (5.0,)

lattice.universes = [
    [pin_universe] * 18,
    [pin_universe] * 12,
    [pin_universe] * 6,
    [pin_universe]
]


#Outer Universe
outer_universe = openmc.Universe(
    name = 'Outer Universe',
    cells = [
        openmc.Cell(
            name = 'Outer Water',
            fill = water
        )
    ]
)

lattice.outer = outer_universe



#-----------------------
# Core
#-----------------------

core_radius = openmc.ZCylinder(
    r=22.098
)

core_top = openmc.ZPlane(
    z0=32.4
)

core_bottom = openmc.ZPlane(
    z0=-32.4
)

core_cell = openmc.Cell(
    name='Core',
    fill=lattice,
    region=-core_radius & +core_bottom & -core_top
)



#-----------------------
# Graphite Reflector
#-----------------------

graphite_reflector = openmc.ZCylinder(
    r = 29.05
)

graphite_reflector_cell = openmc.Cell(
    name = 'Reflector',
    fill = graphite,
    region = +core_radius & -graphite_reflector & -core_top & +core_bottom
)

reflector_region = (+core_radius & -graphite_reflector & -core_top & +core_bottom)



#-----------------------
# Pool
#-----------------------

pool_radius = openmc.ZCylinder(
    r = 96.0,
    boundary_type = 'vacuum'
)

pool_top = openmc.ZPlane(
    z0 = 622.0,
    boundary_type = 'vacuum'
)

pool_bottom = openmc.ZPlane(
    z0 = -40.0,
    boundary_type = 'vacuum'
)


pool = openmc.Cell(
    name = 'Pool',
    fill = water,
    region = -pool_radius & +pool_bottom & -pool_top & ~reflector_region
)



#-----------------------
# Root Universe
#-----------------------

root = openmc.Universe(
    name='Root Universe',
    cells=[core_cell, graphite_reflector_cell, pool]
)

geometry = openmc.Geometry(root)



#=======================
# Settings
#=======================
settings = openmc.Settings()
settings.run_mode = 'eigenvalue'
settings.batches = 100
settings.inactive = 10
settings.particles = 2000



#=======================
# Model
#=======================
model = openmc.Model(
    geometry=geometry,
    materials=materials,
    settings=settings
)



#model.export_to_xml()
model.run()