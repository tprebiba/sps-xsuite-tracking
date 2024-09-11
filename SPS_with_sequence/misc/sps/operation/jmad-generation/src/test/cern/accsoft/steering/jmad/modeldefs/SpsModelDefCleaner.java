/**
 * Copyright (c) 2018 European Organisation for Nuclear Research (CERN), All Rights Reserved.
 */

package cern.accsoft.steering.jmad.modeldefs;

import static cern.accsoft.steering.jmad.tools.modeldefs.cleaning.ModelPackageCleaner.cleanUnusedBelow;

import cern.accsoft.steering.jmad.tools.modeldefs.cleaning.ModelPackageCleaner;

public class SpsModelDefCleaner {

    
    public static void main(String[] args) {
        cleanUnusedBelow("src/java");
    }

}
