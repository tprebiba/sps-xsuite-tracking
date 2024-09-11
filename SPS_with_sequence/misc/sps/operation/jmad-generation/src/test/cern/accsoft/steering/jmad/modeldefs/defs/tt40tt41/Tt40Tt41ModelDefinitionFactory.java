/**
 * 
 */
package cern.accsoft.steering.jmad.modeldefs.defs.tt40tt41;

import cern.accsoft.steering.jmad.domain.file.CallableModelFileImpl;
import cern.accsoft.steering.jmad.domain.file.ModelFile;
import cern.accsoft.steering.jmad.domain.file.ModelPathOffsetsImpl;
import cern.accsoft.steering.jmad.domain.file.CallableModelFile.ParseType;
import cern.accsoft.steering.jmad.domain.file.ModelFile.ModelFileLocation;
import cern.accsoft.steering.jmad.domain.machine.RangeDefinitionImpl;
import cern.accsoft.steering.jmad.domain.machine.SequenceDefinitionImpl;
import cern.accsoft.steering.jmad.domain.machine.filter.RegexNameFilter;
import cern.accsoft.steering.jmad.domain.result.tfs.TfsResult;
import cern.accsoft.steering.jmad.domain.twiss.TwissInitialConditionsImpl;
import cern.accsoft.steering.jmad.domain.types.enums.JMadPlane;
import cern.accsoft.steering.jmad.factory.BeamFactory;
import cern.accsoft.steering.jmad.modeldefs.ModelDefinitionFactory;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinitionImpl;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinitionImpl;

/**
 * This class is the actual model configuration for the AWAKE transfer line.
 * 
 * 
 */
public class Tt40Tt41ModelDefinitionFactory implements ModelDefinitionFactory {

    @Override
    public JMadModelDefinition create() {
        JMadModelDefinitionImpl modelDefinition = new JMadModelDefinitionImpl();
        modelDefinition.setName("TT40TT41");

        ModelPathOffsetsImpl offsets = new ModelPathOffsetsImpl();
        offsets.setResourceOffset("tt40tt41/2016");
        modelDefinition.setModelPathOffsets(offsets);

        modelDefinition.addInitFile(new CallableModelFileImpl("sequence/awaketransfer.seq", ModelFileLocation.RESOURCE));
        modelDefinition.addInitFile(new CallableModelFileImpl("beam/beam_protons.madx", ModelFileLocation.RESOURCE));

        /*
         * OPTICS
         */
        String[] strengthFileNames = new String[] {
               
                "str/awake_protons_2016v1.str",
                "str/awake_protons_2016v2.str",
                "str/awake_protons_2017_sx150_sy325.str",
                "str/awake_protons_2017_sx340_sy140.str",
                "str/awake_protons_2018_sx_sy_400.str",
                "str/awake_protons_2018_sx_sy_500.str"
                
               };
        

        for (String strengthFileName : strengthFileNames) {
            String opticsName = strengthFileName.replaceAll("str/", "").replaceAll(".str", "");
            OpticsDefinition opticsDefinition = new OpticsDefinitionImpl(opticsName,
                    new ModelFile[] { new CallableModelFileImpl(strengthFileName, ModelFileLocation.RESOURCE,
                            ParseType.STRENGTHS) });
            modelDefinition.addOpticsDefinition(opticsDefinition);
        }
        modelDefinition.setDefaultOpticsDefinition(modelDefinition.getOpticsDefinitions().get(0));

        /*
         * SEQUENCE
         */

       
        SequenceDefinitionImpl awakeline = new SequenceDefinitionImpl("tt40tt41",null);
        modelDefinition.setDefaultSequenceDefinition(awakeline);
        RangeDefinitionImpl awakelinerange = new RangeDefinitionImpl(awakeline, "ALL", createAWAKEInitialConditions());
        awakeline.setDefaultRangeDefinition(awakelinerange);

        return modelDefinition;
    }

    /**
     * Twiss initial conditions for transferline AWAKE
     */
    private final TwissInitialConditionsImpl createAWAKEInitialConditions() {
        TwissInitialConditionsImpl twissInitialConditions = new TwissInitialConditionsImpl("awake-twiss");

       
       
        
        twissInitialConditions.setDeltap(0.0);
        twissInitialConditions.setBetx(27.931086);
        twissInitialConditions.setAlfx(0.650549);
        twissInitialConditions.setDx(-0.557259);
        twissInitialConditions.setDpx(0.013567);
        twissInitialConditions.setBety(120.056512);
        twissInitialConditions.setAlfy(-2.705071);
        twissInitialConditions.setDy(0.0);
        twissInitialConditions.setDpy(0.0);
        twissInitialConditions.setCalcAtCenter(true);
        twissInitialConditions.setClosedOrbit(false);
        return twissInitialConditions;
        
        


    }

}
