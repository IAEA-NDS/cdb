<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:c="https://www-amdis.iaea.org/cdbml">

<xsl:template match="/">
CDB Record <xsl:value-of select="/c:cdbml/c:cdbrecord/@id"/>
=================

    <xsl:for-each select="/c:cdbml/c:cdbrecord/c:attribution">
Attribution <xsl:value-of select="@id"/>
-=-=-=-=-=-=-=-=-
Contributor
-----------
<xsl:value-of select="c:name"/>, <xsl:value-of select="c:affiliation"/>
Publication
-----------
Publication DOI: http://doi.org/<xsl:value-of select="c:doi"/>

Acknowledgements
----------------
<xsl:value-of select="c:acknowledgements"/>

</xsl:for-each>

    <xsl:for-each select="/c:cdbml/c:cdbrecord/c:material">
Material
-=-=-=-=
Formula:<xsl:value-of select="c:formula"/>
Structure: <xsl:value-of select="c:structure"/>
<xsl:apply-templates select="c:lattice_parameters"/>

Simulation includes surface? <xsl:value-of select="/c:cdbml/c:cdbrecord/c:has_surface" />
Initially perfect crystal configuration? <xsl:value-of select="/c:cdbml/c:cdbrecord/c:initially_perfect" />
    </xsl:for-each>

PKA
-=-
PKA atomic number: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA_atomic_number" />
PKA energy: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA/c:energy" /> <xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA/c:energy/@units" />
PKA by recoil? <xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA/c:recoil" />

Simulation Details
-=-=-=-=-=-=-=-=-=
Electronic stopping included? <xsl:value-of select="/c:cdbml/c:cdbrecord/c:electronic_stopping" />
Electronic stopping comments: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:electronic_stopping_comment" />

Thermostat? <xsl:value-of select="/c:cdbml/c:cdbrecord/c:thermostat" />
Thermostat comments: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:thermostat_comment" />

Input filename: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:input_filename" />

Simulation time: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_time" /> <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_time/@units" />

Initial temperature: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:initial_temperature" /> <xsl:value-of select="/c:cdbml/c:cdbrecord/c:initial_temperature/@units" />

Box dimensions (Å): <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_X_length"/>, <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_Y_length"/>, <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_Z_length"/>

<xsl:if test="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_orientation">Box orientation:
    <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_orientation/c:X_orientation"/>,
    <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_orientation/c:Y_orientation"/>,
    <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_orientation/c:Z_orientation"/>
</xsl:if>

Interatomic potential filename: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:interatomic_potential/c:filename" />
Interatomic potential comment: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:interatomic_potential/c:comment" />

Code: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:code/c:name" /> Version: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:code/c:version" />

Data
-=-=
Data archive name: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:data/c:archive_name" />

Columns
-------
Position | Name | Units
<xsl:for-each select="/c:cdbml/c:cdbrecord/c:data/c:columns/c:column">
<xsl:value-of select="position()" /> | <xsl:value-of select="c:name" /> | <xsl:value-of select="c:units" />
</xsl:for-each>

Comments
--------
<xsl:value-of select="/c:cdbml/c:cdbrecord/c:data/c:comments" />

</xsl:template>

<xsl:template match="c:lattice_parameters">
    a = <xsl:value-of select="c:a"/> <xsl:value-of select="c:a/@units"/>,
    b = <xsl:value-of select="c:b"/> <xsl:value-of select="c:b/@units"/>,
    c = <xsl:value-of select="c:c"/> <xsl:value-of select="c:c/@units"/>.
    α = <xsl:value-of select="c:alpha"/><xsl:choose><xsl:when test="c:alpha/@units='deg'">°</xsl:when><xsl:otherwise> <xsl:value-of select="c:alpha/@units"/></xsl:otherwise></xsl:choose>,
    β = <xsl:value-of select="c:beta"/><xsl:choose><xsl:when test="c:beta/@units='deg'">°</xsl:when><xsl:otherwise> <xsl:value-of select="c:beta/@units"/></xsl:otherwise></xsl:choose>,
    γ = <xsl:value-of select="c:gamma"/><xsl:choose><xsl:when test="c:gamma/@units='deg'">°</xsl:when><xsl:otherwise> <xsl:value-of select="c:gamma/@units"/></xsl:otherwise></xsl:choose>.
    
</xsl:template>

</xsl:stylesheet>
