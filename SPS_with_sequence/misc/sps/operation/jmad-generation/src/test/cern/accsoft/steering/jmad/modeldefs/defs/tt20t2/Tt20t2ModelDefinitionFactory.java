/**
 * 
 */
package cern.accsoft.steering.jmad.modeldefs.defs.tt20t2;

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
 * This class is the actual model configuration for the TT20T2 transfer line.
 * 
 * @author Kajetan Fuchsberger (kajetan.fuchsberger at cern.ch)
 */
public class Tt20t2ModelDefinitionFactory implements ModelDefinitionFactory {

    @Override
    public JMadModelDefinition create() {
        JMadModelDefinitionImpl modelDefinition = new JMadModelDefinitionImpl();
        modelDefinition.setName("TT20T2");

        ModelPathOffsetsImpl offsets = new ModelPathOffsetsImpl();
        offsets.setResourceOffset("tt20t2/2015");
        modelDefinition.setModelPathOffsets(offsets);

        modelDefinition.addInitFile(new CallableModelFileImpl("beam/beam.madx", ModelFileLocation.RESOURCE));
        modelDefinition.addInitFile(new CallableModelFileImpl("sequence/tt20t2.seq", ModelFileLocation.RESOURCE));

        /*
         * OPTICS
         */
        String[] strengthFileNames = new String[] {
                "str/t2_pb_lowenergy_vert_ll.str",
                "str/t2_pb_lowenergy.str",
                "str/t2_protons_SE_noqsplit_vert_ll.str",
                "str/t2_protons_SE_noqsplit.str"
               };
        

        for (String strengthFileName : strengthFileNames) {
            String opticsName = strengthFileName.replaceAll("str/t2_", "tt20t2_2015_").replaceAll(".str", "");
            OpticsDefinition opticsDefinition = new OpticsDefinitionImpl(opticsName,
                    new ModelFile[] { new CallableModelFileImpl(strengthFileName, ModelFileLocation.RESOURCE,
                            ParseType.STRENGTHS) });
            modelDefinition.addOpticsDefinition(opticsDefinition);
        }
        modelDefinition.setDefaultOpticsDefinition(modelDefinition.getOpticsDefinitions().get(0));

        /*
         * SEQUENCE
         */

       
        SequenceDefinitionImpl tt20t2 = new SequenceDefinitionImpl("tt20t2",null);
        modelDefinition.setDefaultSequenceDefinition(tt20t2);
        RangeDefinitionImpl tt20t2range = new RangeDefinitionImpl(tt20t2, "ALL", createTT20T2InitialConditions());
        tt20t2.setDefaultRangeDefinition(tt20t2range);

        return modelDefinition;
    }

    /**
     * Twiss initial conditions for transferline TT20T2
     */
    private final TwissInitialConditionsImpl createTT20T2InitialConditions() {
        TwissInitialConditionsImpl twissInitialConditions = new TwissInitialConditionsImpl("tt20t2-twiss");

     
      
        
        twissInitialConditions.setDeltap(0.0);
        twissInitialConditions.setBetx(46.4144684);
        twissInitialConditions.setAlfx(-3.087019543);
        twissInitialConditions.setDx(-0.229082543);
        twissInitialConditions.setDpx(0.01358783731);
        twissInitialConditions.setBety(117.3299884);
        twissInitialConditions.setAlfy(-3.251188218);
        twissInitialConditions.setDy(0.289);
        twissInitialConditions.setDpy(0.00348);
        twissInitialConditions.setCalcAtCenter(true);
        twissInitialConditions.setClosedOrbit(false);
        return twissInitialConditions;

    }

}
