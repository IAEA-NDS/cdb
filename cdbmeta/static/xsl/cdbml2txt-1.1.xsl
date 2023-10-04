<?xml version="1.0"?>

<xsl:stylesheet version="1.1" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:c="https://amdis.iaea.org/cdbml">
<xsl:output method="text" />
<xsl:variable name="newline" select="'&#xD;&#xA;'" />
<xsl:template match="/">
<xsl:text>CDB Record </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/@id"/><xsl:value-of select="$newline"/>
<xsl:text>=================</xsl:text><xsl:value-of select="$newline"/>
<xsl:value-of select="$newline"/>
<xsl:for-each select="/c:cdbml/c:cdbrecord/c:attribution">
<xsl:text>Attribution </xsl:text><xsl:value-of select="@id"/><xsl:value-of select="$newline"/>
<xsl:text>=================</xsl:text><xsl:value-of select="$newline"/>
<xsl:value-of select="$newline"/>
<xsl:text>Contributor: </xsl:text><xsl:value-of select="c:name"/>, <xsl:value-of select="c:affiliation"/><xsl:value-of select="$newline"/>
<xsl:text>Publication DOI: https://doi.org/</xsl:text><xsl:value-of select="c:doi"/>
<xsl:value-of select="$newline"/><xsl:value-of select="$newline"/>
<xsl:text>Acknowledgements
----------------</xsl:text>
<xsl:value-of select="$newline"/>
<xsl:value-of select="c:acknowledgements"/>
<xsl:value-of select="$newline"/>
</xsl:for-each>
<xsl:value-of select="$newline"/>
<xsl:for-each select="/c:cdbml/c:cdbrecord/c:material">
<xsl:text>Material
========</xsl:text><xsl:value-of select="$newline"/>
<xsl:text>Formula: </xsl:text><xsl:value-of select="c:formula"/><xsl:value-of select="$newline"/>
<xsl:text>Structure: </xsl:text><xsl:value-of select="c:structure"/><xsl:value-of select="$newline"/>
<xsl:apply-templates select="c:lattice_parameters"/>
<xsl:text>Simulation includes surface? </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:has_surface" /><xsl:value-of select="$newline"/>
<xsl:text>Initially perfect crystal configuration? </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:initially_perfect" /><xsl:value-of select="$newline"/>
<xsl:value-of select="$newline"/>
</xsl:for-each>
<xsl:text>PKA
===
PKA atomic number: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA_atomic_number" /><xsl:value-of select="$newline"/>
<xsl:text>PKA energy: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA/c:energy" /> <xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA/c:energy/@units" /><xsl:value-of select="$newline"/>
<xsl:text>PKA by recoil? </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA/c:recoil" /><xsl:value-of select="$newline"/>
<xsl:value-of select="$newline"/>
<xsl:text>Simulation Details
==================
Electronic stopping included? </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:electronic_stopping" /><xsl:value-of select="$newline"/>
<xsl:text>Electronic stopping comments: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:electronic_stopping_comment" /><xsl:value-of select="$newline"/>
<xsl:text>Thermostat? </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:thermostat" /><xsl:value-of select="$newline"/>
<xsl:text>Thermostat comments: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:thermostat_comment" /><xsl:value-of select="$newline"/>
<xsl:text>Input filename: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:input_filename" /><xsl:value-of select="$newline"/>
<xsl:text>Simulation time: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_time" /> <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_time/@units" /><xsl:value-of select="$newline"/>
<xsl:text>Initial temperature: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:initial_temperature" /> <xsl:value-of select="/c:cdbml/c:cdbrecord/c:initial_temperature/@units" /><xsl:value-of select="$newline"/>
<xsl:text>Box dimensions (Å): </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_X_length"/>, <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_Y_length"/>, <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_Z_length"/><xsl:value-of select="$newline"/>

<xsl:if test="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_orientation">
<xsl:text>Box orientation: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_orientation/c:X_orientation"/>, <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_orientation/c:Y_orientation"/>, <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_orientation/c:Z_orientation"/><xsl:value-of select="$newline"/>
</xsl:if>
<xsl:text>Interatomic potential URI: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:interatomic_potential/c:uri" /><xsl:value-of select="$newline"/>
<xsl:text>Interatomic potential filename: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:interatomic_potential/c:filename" /><xsl:value-of select="$newline"/>
<xsl:text>Interatomic potential comment: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:interatomic_potential/c:comment" /><xsl:value-of select="$newline"/>
<xsl:text>Interatomic potential doi: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:interatomic_potential/c:doi" /><xsl:value-of select="$newline"/>
<xsl:text>Code: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:code/c:name" /> Version: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:code/c:version" /><xsl:value-of select="$newline"/>
<xsl:value-of select="$newline"/>
<xsl:text>Data
====</xsl:text><xsl:value-of select="$newline"/>
<xsl:text>Data archive name: </xsl:text><xsl:value-of select="/c:cdbml/c:cdbrecord/c:data/c:archive_name" /><xsl:value-of select="$newline"/>
<xsl:value-of select="$newline"/>
<xsl:text>Comments
--------</xsl:text><xsl:value-of select="$newline"/>
<xsl:value-of select="/c:cdbml/c:cdbrecord/c:data/c:comments" />

</xsl:template>

<xsl:template match="c:lattice_parameters">
<xsl:text>Lattice Parameters:</xsl:text>
    a = <xsl:value-of select="c:a"/> <xsl:value-of select="c:a/@units"/>,
    b = <xsl:value-of select="c:b"/> <xsl:value-of select="c:b/@units"/>,
    c = <xsl:value-of select="c:c"/> <xsl:value-of select="c:c/@units"/>.
    α = <xsl:value-of select="c:alpha"/><xsl:choose><xsl:when test="c:alpha/@units='deg'">°</xsl:when><xsl:otherwise> <xsl:value-of select="c:alpha/@units"/></xsl:otherwise></xsl:choose>,
    β = <xsl:value-of select="c:beta"/><xsl:choose><xsl:when test="c:beta/@units='deg'">°</xsl:when><xsl:otherwise> <xsl:value-of select="c:beta/@units"/></xsl:otherwise></xsl:choose>,
    γ = <xsl:value-of select="c:gamma"/><xsl:choose><xsl:when test="c:gamma/@units='deg'">°</xsl:when><xsl:otherwise> <xsl:value-of select="c:gamma/@units"/></xsl:otherwise></xsl:choose>.
</xsl:template>

</xsl:stylesheet>
