/**
 * Copyright (c) 2018 European Organisation for Nuclear Research (CERN), All Rights Reserved.
 */

package cern.accsoft.steering.jmad.modeldefs;

import static cern.accsoft.steering.jmad.tools.modeldefs.creating.ModelDefinitionCreator.scanDefault;
/*
 * This function looks in the path for model definition factories and creates xml files
 * 
 * https://gitlab.cern.ch/jmad-modelpacks-cern/docs/blob/master/using-jmad-modeldefs-dsl.md
 */
public class SpsModelDefCreator {

    public static void main(String[] args) {
        scanDefault().and().writeTo("..");
    }

}
