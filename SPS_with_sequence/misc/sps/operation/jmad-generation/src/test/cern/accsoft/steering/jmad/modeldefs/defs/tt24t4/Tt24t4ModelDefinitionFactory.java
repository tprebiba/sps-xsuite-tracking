/**
 * 
 */
package cern.accsoft.steering.jmad.modeldefs.defs.tt24t4;

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
 * This class is the actual model configuration for the TT24T4 transfer line.
 * 
 * 
 */
public class Tt24t4ModelDefinitionFactory implements ModelDefinitionFactory {

    @Override
    public JMadModelDefinition create() {
        JMadModelDefinitionImpl modelDefinition = new JMadModelDefinitionImpl();
        modelDefinition.setName("TT24T4");

        ModelPathOffsetsImpl offsets = new ModelPathOffsetsImpl();
        offsets.setResourceOffset("tt24t4/2015");
        modelDefinition.setModelPathOffsets(offsets);

        modelDefinition.addInitFile(new CallableModelFileImpl("beam/beam.madx", ModelFileLocation.RESOURCE));
        modelDefinition.addInitFile(new CallableModelFileImpl("sequence/tt24t4.seq", ModelFileLocation.RESOURCE));

        /*
         * OPTICS
         */
        String[] strengthFileNames = new String[] {
               
                "str/t4_protons_SE_noqsplit_vert_ll.str",
                "str/t4_protons_SE_noqsplit.str"
               };
        

        for (String strengthFileName : strengthFileNames) {
            String opticsName = strengthFileName.replaceAll("str/t4_", "tt24t4_2015_").replaceAll(".str", "");
            OpticsDefinition opticsDefinition = new OpticsDefinitionImpl(opticsName,
                    new ModelFile[] { new CallableModelFileImpl(strengthFileName, ModelFileLocation.RESOURCE,
                            ParseType.STRENGTHS) });
            modelDefinition.addOpticsDefinition(opticsDefinition);
        }
        modelDefinition.setDefaultOpticsDefinition(modelDefinition.getOpticsDefinitions().get(0));

        /*
         * SEQUENCE
         */

       
        SequenceDefinitionImpl tt24t4 = new SequenceDefinitionImpl("tt24t4",null);
        modelDefinition.setDefaultSequenceDefinition(tt24t4);
        RangeDefinitionImpl tt24t4range = new RangeDefinitionImpl(tt24t4, "ALL", createTT24T4InitialConditions());
        tt24t4.setDefaultRangeDefinition(tt24t4range);

        return modelDefinition;
    }

    /**
     * Twiss initial conditions for transferline TT24T4
     */
    private final TwissInitialConditionsImpl createTT24T4InitialConditions() {
        TwissInitialConditionsImpl twissInitialConditions = new TwissInitialConditionsImpl("tt24t4-twiss");

        twissInitialConditions.setDeltap(0.0);
        twissInitialConditions.setBetx(17.08204323);
        twissInitialConditions.setAlfx(0.8280252328);
        twissInitialConditions.setDx(-0.6251331317);
        twissInitialConditions.setDpx(0.03107025437);
        twissInitialConditions.setBety(23601.70867);
        twissInitialConditions.setAlfy(-1.765036154);
        twissInitialConditions.setDy(0.3991115509);
        twissInitialConditions.setDpy(-0.001105971255);
        twissInitialConditions.setCalcAtCenter(true);
        twissInitialConditions.setClosedOrbit(false);
        return twissInitialConditions;
        
        


    }

}
