/**
 * 
 */
package cern.accsoft.steering.jmad.modeldefs.defs.tt25t6;

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
 * This class is the actual model configuration for the TT25T6 transfer line.
 * 
 * @author Kajetan Fuchsberger (kajetan.fuchsberger at cern.ch)
 */
public class Tt25t6ModelDefinitionFactoryIons implements ModelDefinitionFactory {

    @Override
    public JMadModelDefinition create() {
        JMadModelDefinitionImpl modelDefinition = new JMadModelDefinitionImpl();
        modelDefinition.setName("TT25T6IONS");

        ModelPathOffsetsImpl offsets = new ModelPathOffsetsImpl();
        offsets.setResourceOffset("tt25t6/2015");
        modelDefinition.setModelPathOffsets(offsets);

        modelDefinition.addInitFile(new CallableModelFileImpl("beam/beam.madx", ModelFileLocation.RESOURCE));
        modelDefinition.addInitFile(new CallableModelFileImpl("sequence/tt25t6.seq", ModelFileLocation.RESOURCE));

        /*
         * OPTICS
         */
        String[] strengthFileNames = new String[] {
                "str/t6_pb_lowenergy_vert_ll.str",
                "str/t6_pb_lowenergy.str"
                
               };
        

        for (String strengthFileName : strengthFileNames) {
            String opticsName = strengthFileName.replaceAll("str/t6_", "tt25t6_2015_").replaceAll(".str", "");
            OpticsDefinition opticsDefinition = new OpticsDefinitionImpl(opticsName,
                    new ModelFile[] { new CallableModelFileImpl(strengthFileName, ModelFileLocation.RESOURCE,
                            ParseType.STRENGTHS) });
            modelDefinition.addOpticsDefinition(opticsDefinition);
        }
        modelDefinition.setDefaultOpticsDefinition(modelDefinition.getOpticsDefinitions().get(0));

        /*
         * SEQUENCE
         */

       
        SequenceDefinitionImpl tt25t6 = new SequenceDefinitionImpl("tt25t6",null);
        modelDefinition.setDefaultSequenceDefinition(tt25t6);
        RangeDefinitionImpl tt25t6range = new RangeDefinitionImpl(tt25t6, "ALL", createTT25T6InitialConditions());
        tt25t6.setDefaultRangeDefinition(tt25t6range);

        return modelDefinition;
    }

    /**
     * Twiss initial conditions for transferline TT25T6
     */
    private final TwissInitialConditionsImpl createTT25T6InitialConditions() {
        TwissInitialConditionsImpl twissInitialConditions = new TwissInitialConditionsImpl("tt25t6-twiss");

        twissInitialConditions.setDeltap(0.0);
        twissInitialConditions.setBetx(6.269211626);
        twissInitialConditions.setAlfx(0.9476579136);
        twissInitialConditions.setDx(0.6755795062);
        twissInitialConditions.setDpx(-0.02490174268);
        twissInitialConditions.setBety(4517.380062);
        twissInitialConditions.setAlfy(0.05749480438);
        twissInitialConditions.setDy(0.03188050602);
        twissInitialConditions.setDpy(-0.0005434036736);
        twissInitialConditions.setCalcAtCenter(true);
        twissInitialConditions.setClosedOrbit(false);
        return twissInitialConditions;
       
    }

}
